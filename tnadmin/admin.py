# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.
# Copyright (c) The django-ldapdb project


from django import forms
from django.contrib import admin


from tnadmin.models.gvOrg import gvOrgUnit, gvOrganisation

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
    form = gvOrgUnitForm
    readonly_fields = ('gvSource', )
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
    #exclude = ['dn']
    list_display = ['gvOuID', 'gvOuVKZ', 'ou']
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
    form = gvOrganisationForm
    readonly_fields = ('gvSource', )
    exclude = ('gvOuIdParent', )
    fields = (
        'gvOuID',
        'gvOuVKZ',
        'o',
        'cn',
        'gvOuCn',
        'location',
        'mail',
        'description',
        'gvNotValidBefore',
        'gvNotValidAfter',
        'gvStatus',
        'gvSource',
    )
    list_display = ['gvOuID', 'gvOuVKZ', 'o']
    #search_fields = ['first_name', 'last_name', 'full_name']
