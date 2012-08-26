from datetime import datetime, timedelta

from django.conf import settings
from django.views.generic import FormView
from django.forms.util import ErrorList
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext

from django.core.mail import EmailMessage, get_connection

from contactform.forms import ContactForm
from contactform.models import ContactLog
from contactform.exceptions import EmailThrottled


class ContactView(FormView):
    template_name = 'contactform/contact_form.html'
    body_template_name = 'contactform/email_body.txt'
    success_url = "."
    form_class = ContactForm
    recipients = [u"{0}<{1}>".format(name, email)
                  for name, email in settings.MANAGERS]
    messages_per_minute = 3
    messages_per_hour = 10

    def form_valid(self, form):
        try:
            self.send_email(form)
        except EmailThrottled:
            errors = form._errors.setdefault('__all__', ErrorList())
            errors.append(ugettext("You are only allowed to send {0} messages"
                                   " per minute and {1} per hour.")
                .format(self.messages_per_minute, self.messages_per_hour))
            log = ContactLog(email=form.cleaned_data['email'],
                ip=self.request.META.get('REMOTE_ADDR', '0.0.0.0'),
                date=datetime.now(), status='T')
            log.save()
            return self.form_invalid(form)

        return super(ContactView, self).form_valid(form)

    def sending_allowed(self, form):
        ip = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
        last_minute = ContactLog.objects.filter(
            date__gte=timezone.now() - timedelta(minutes=1), ip=ip).count()
        last_hour = ContactLog.objects.filter(
            date__gte=timezone.now() - timedelta(hours=1), ip=ip).count()

        return (last_minute < self.messages_per_minute)\
            and (last_hour < self.messages_per_hour)

    def get_recipients(self, form):
        return self.recipients

    def get_headers(self, form):
        return {}

    def get_body_context(self, form):
        return {}

    def get_body_template(self, form):
        return get_template(self.body_template_name)

    def get_subject(self, form):
        raise NotImplementedError

    def get_from_email(self, form):
        raise NotImplementedError

    def get_body(self, form):
        context_dir = {
            'form': form,
            'fields': form.cleaned_data
        }
        context_dir.update(self.get_body_context(form))
        context = Context(context_dir)
        body_template = self.get_body_template(form)
        return body_template.render(context)

    def send_email(self, form):
        if not self.sending_allowed(form):
            raise EmailThrottled

        connection = get_connection(fail_silently=False)

        email = EmailMessage(
            subject=self.get_subject(form),
            body=self.get_body(form),
            from_email=self.get_from_email(form),
            to=self.get_recipients(form),
            headers=self.get_headers(form),
            connection=connection
        )
        sent = email.send()

        if sent:
            log = ContactLog(email=form.cleaned_data['email'],
                ip=self.request.META.get('REMOTE_ADDR', '0.0.0.0'),
                date=datetime.now(), status='S')
            log.save()
