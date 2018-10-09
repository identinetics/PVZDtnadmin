from django import forms
from django.contrib import admin
from portaladmin.models.MDstatement import *
from ..signals import md_statement_edit_starts


class MDstatementForm(forms.ModelForm):

    class Meta:
        model = MDstatement
        exclude = ['checkout_status']


@admin.register(MDstatement)
class MDstatementAdmin(admin.ModelAdmin):
    form = MDstatementForm
    actions = None
    list_display = ['entityID', 'Status']
    readonly_fields = list_display
    search_fields = ('entityID', 'Status', )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        md_statement_edit_starts.send(sender=MDstatement, md_statement_id=object_id)
        # TODO if we found another user status then block then form loading
        return super().change_view(request, object_id, form_url, extra_context)


