from django import forms
from django.contrib import admin
from tnadmin.models.gvOrg import *

class gvOrgUnitForm(forms.ModelForm):
    class Meta(object):
        widgets = {
            'gvOuID': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuVKZ': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuCn': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
        }

@admin.register(gvOrgUnit)
class gvOrgUnitAdmin(admin.ModelAdmin):
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
    form = gvOrgUnitForm
    list_display = ['gvOuID', 'gvOuVKZ', 'ou']
    readonly_fields = ('gvSource', )
    #search_fields = ['first_name', 'last_name', 'full_name']

class gvOrganisationForm(forms.ModelForm):
    class Meta(object):
        #model = gvOrganisation
        widgets = {
            'gvOuID': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuVKZ': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'gvOuCn': forms.Textarea(attrs={'rows':2, 'cols':80}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':80}),
        }

@admin.register(gvOrganisation)
class gvOrganisationAdmin(admin.ModelAdmin):
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
    form = gvOrganisationForm
    list_display = ['gvOuID', 'gvOuVKZ', 'cn']
    readonly_fields = ('gvSource', )
    #search_fields = ['first_name', 'last_name', 'full_name']
