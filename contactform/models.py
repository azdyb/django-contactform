from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

STATUS_CHOICES = (
    ('U', _("Unknown")),
    ('S', _("Sent")),
    ('T', _("Throttled"))
)

class ContactLog(models.Model):
    ip = models.IPAddressField(verbose_name=_("IP"))
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    status = models.CharField(verbose_name=_("Status"), max_length=1,
        choices=STATUS_CHOICES)

    class Meta:
        verbose_name = _("Contact Log")
        verbose_name_plural = _("Contact Logs")

    def __unicode__(self):
        return ugettext("{0} at {1}").format(self.ip,
            timezone.localtime(self.date))
