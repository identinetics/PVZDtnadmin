from django import forms
from django.contrib import admin
from tnadmin.models.gvOrg import *

class GvOrgUnitForm(forms.ModelForm):
    class Meta(object):
        widgets = {
            'gvOuID': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuVKZ': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuCn': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
        }

@admin.register(GvOrgUnit)
class GvOrgUnitAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'gvOuID',
        'gvOuVKZ',
        'ou',
        'cn',
        'gvOuCn',
        'gvOuIdParent',
        'location',
        'mail',
        'description',
        'gvNotValidBefore',
        'gvNotValidAfter',
        'gvStatus',
        'gvSource',
    )
    form = GvOrgUnitForm
    list_display = ['gvOuID', 'gvOuVKZ', 'ou']
    readonly_fields = ('gvSource', )
    #search_fields = ['first_name', 'last_name', 'full_name']

class GvOrganisationForm(forms.ModelForm):
    class Meta(object):
        #model = gvOrganisation
        widgets = {
            'gvOuID': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuVKZ': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuCn': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
        }

@admin.register(GvOrganisation)
class GvOrganisationAdmin(admin.ModelAdmin):
    actions = None
    exclude = ('gvOuIdParent', )
    fields = (
        'gvOuID',
        'gvOuVKZ',
        'o',
        'cn',
        'location',
        'mail',
        'description',
        'gvNotValidBefore',
        'gvNotValidAfter',
        'gvStatus',
        'gvSource',
    )
    form = GvOrganisationForm
    list_display = ['gvOuID', 'gvOuVKZ', 'cn']
    readonly_fields = ('gvSource', )
    #search_fields = ['first_name', 'last_name', 'full_name']
