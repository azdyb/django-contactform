from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=254)
    email = forms.EmailField(label=_("E-mail"))
    body = forms.CharField(label=_("Contents"), max_length=1000,
        widget=forms.Textarea)
