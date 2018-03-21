from django import forms
from django.contrib import admin
from tnadmin.models.gvFederation import *


@admin.register(gvFederation)
class gvFederationAdmin(admin.ModelAdmin):
    readonly_fields = ('gvSource', )
    fields = (
        'gvFederationName',
        'gvMetaDataURL',
        'gvStatus',
        'gvSource',
    )
    list_display = ['gvFederationName', 'gvMetaDataURL', 'gvStatus', 'gvSource']
    actions = None
