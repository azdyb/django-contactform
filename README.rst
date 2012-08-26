What is django-contactform?
===========================

django-contactform is an Django application providing generic,
class-based contact form.

It is full-featured, ready to use application that lets quickly add
a contact form to the service. It comes with built-in feature to
send emails to managers/webmasters and throttling option to prevent spamming.


Usage
=====

Obligatory steps
----------------

To get started one needs to subclass ``views.ContactView`` and override
both of the following methods:

* ``get_subject``,
* ``get_from_email``.

For example::

    from contactform.views import ContactView

    class MyContactView(ContactView):
        def get_subject(self, form):
            return "Contact from MySite"

        def get_from_email(self, form):
            return "MySite <no-reply@example.com>"


Next step is to create two templates:

* ``contactform/contact_form.html`` – renders the form,
* ``contactform/email_body.txt`` – renders the body of an e-mail sent to
  recipients.

The ``email_body.txt`` template's context is populated with ``form``
and ``fields`` variables, which are submitted and validated form
and ``form.cleaned_data`` respectively. Note, that ``fields`` variable is
provided only for convenience and ``form.cleaned_data`` might be used as well.


One must also configure e-mail sending in Django settings. In most cases
setting ``EMAIL_HOST``, ``EMAIL_HOST_USER`` and ``EMAIL_HOST_PASSWORD`` will do.
For more information, please consult `Django documentation about settings`_.

.. _Django documentation about settings:
    https://docs.djangoproject.com/en/dev/ref/settings/


Optional steps
--------------

Recipients list defaults to list derived from ``settings.MANAGERS``,
but it may be changed by overriding ``recipients`` class variable
or ``get_recipients`` method.


Additional e-mail headers may be added by overriding ``get_headers`` method.
One common reason to do this is to provide ``Reply-To`` header. For example::

    class MyContactView(ContactView):
        def get_headers(self, form):
            return  {'Reply-To': u"{0}<{1}>".format(form.cleaned_data['name'], form.cleaned_data['email'])}

This will result in setting ``Reply-To`` header to name and e-mail provided
by the user submitting the form.


Throttling settings default to 3 e-mails per minute and 10 per hour. It's
configurable by overriding ``messages_per_minute`` and ``messages_per_hour``
class variables or – for more control – ``sending_allowed`` method.


Logs
====

django-contactform logs every submission of the form by creating
``models.ContactLog``. It stores information about IP and e-mail along with
date and status (message sent or throttled).

These logs are used internally to decide if the submission quota was
exceeded or not, but may also be used to detect abuses.


What it looks like?
===================

Everybody loves screenshots, right? But actually the look of the form
depends on how designer styles it. Here is humble example to show the idea.

Rendered form:

.. image:: http://img846.imageshack.us/img846/8231/contactlogform.png
  :alt: Rendered form


And some screenshots of admin showing ContactLogs.

Admin list view:

.. image:: http://img217.imageshack.us/img217/3503/contactloglistview.png
  :alt: Admin list view


Admin item view:

.. image:: http://img543.imageshack.us/img543/2531/contactlogchangeview.png
  :alt: Admin item view


Installation
============

django-contactform is installed just like any other Django application:

1. Put *contactform* directory in any path, where python can find it
2. Add *contactform* to ``installed_apps`` in settings.py
3. Run ```manage.py syncdb``` to create database tables for contactform logs
4. (optional) Register ModelAdmin classes found in ``contactform/admin.py`` file in your admin site


License
=======

Copyright (c) 2012, Aleksander Zdyb
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
