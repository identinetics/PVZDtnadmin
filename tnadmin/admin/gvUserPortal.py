from django import forms
from django.contrib import admin
from tnadmin.models.gvUserPortal import *


class GvUserPortalForm(forms.ModelForm):
    class Meta(object):
        #model = gvOrganisation
        widgets = {
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'gvPortalHotlineMail': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'gvAdminContactName': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'gvAdminContactMail': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'gvAdminContactTel': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
        }


@admin.register(GvUserPortal)
class GvUserPortalAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'cn',
        'gvouid_owner',
        'gvouid_participant',
        'gvSamlIdpEntityId',
        'gvMaxSecClass',
        'description',
        'gvPortalHotlineMail',
        'gvAdminContactName',
        'gvAdminContactMail',
        'gvAdminContactTel',
        'gvStatus',
        'gvSource',
    )
    autocomplete_fields = ('gvouid_owner', )
    filter_horizontal = ('gvouid_participant', )
    form = GvUserPortalForm
    list_display = ['cn', 'gvouid_owner', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )
