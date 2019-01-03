from django import forms
from django.contrib import admin
from tnadmin.models.gvorg import *

class GvOrganisationForm(forms.ModelForm):
    class Meta(object):
        #model = gvOrganisation
        widgets = {
            'gvOuId': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuVKZ': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuCn': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
        }

@admin.register(GvOrganisation)
class GvOrganisationAdmin(admin.ModelAdmin):
    actions = None
    exclude = ('gvOuIdParent', )
    fields = (
        'gvOuId',
        'gvOuVKZ',
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
    list_display = ['gvOuId', 'gvOuVKZ', 'o', 'cn', 'gvStatus', 'gvSource']
    #list_editable = ['gvOuId', 'gvOuVKZ', 'cn']
    #list_display_links = ['o' ]
    readonly_fields = ('gvSource', )
    search_fields = (
        'gvOuId',
        'gvOuVKZ',
        'o',
        'cn',
        'l',
        'mail',
        'gvNotValidBefore',
        'gvNotValidAfter',
        'gvStatus',
    )
