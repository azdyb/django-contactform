from django.contrib import admin

from contactform.models import ContactLog


class ContactLogAdmin(admin.ModelAdmin):
    readonly_fields = ('ip', 'email', 'date', 'status')
    fields = ('ip', 'email', 'date', 'status')
    list_filter = ('ip', 'email', 'date', 'status')
    list_display = ('ip', 'email', 'date', 'status')


admin.site.register(ContactLog, ContactLogAdmin)
