from django.contrib import admin

from contactform.models import ContactLog


class ContactLogAdmin(admin.ModelAdmin):
    readonly_fields = ('ip', 'date', 'status')
    fields = ('ip', 'date', 'status')
    list_filter = ('ip', 'date', 'status')
    list_display = ('ip', 'date', 'status')


admin.site.register(ContactLog, ContactLogAdmin)
