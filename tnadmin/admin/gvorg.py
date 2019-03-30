from django import forms
from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin
from tnadmin.models.gvorg import *

class GvOrganisationForm(forms.ModelForm):
    class Meta(object):
        #model = gvOrganisation
        widgets = {
            'gvouid': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvouvkz': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuCn': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
        }

@admin.register(GvOrganisation)
class GvOrganisationAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    #actions = None
    exclude = ('gvouidparent', )
    fields = (
        'gvouid',
        'gvouvkz',
        'ldap_dn',
        'o',
        'cn',
        'l',
        'mail',
        'description',
        'gvNotValidBefore',
        'gvNotValidAfter',
        'gvStatus',
        'gvSource',
    )
    form = GvOrganisationForm
    list_display = ['ldap_dn', 'gvouid', 'gvouvkz', 'o', 'cn', 'gvStatus', 'gvSource']
    #list_editable = ['gvouid', 'gvouvkz', 'cn']
    #list_display_links = ['o' ]
    readonly_fields = ('gvSource', )
    search_fields = (
        'gvouid',
        'gvouvkz',
        'o',
        'cn',
        'l',
        'mail',
        'gvNotValidBefore',
        'gvNotValidAfter',
        'gvStatus',
    )
    changelist_links = ['STPbetreiber']
