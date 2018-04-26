from django import forms
from django.contrib import admin
from tnadmin.models.gvFederation import *


@admin.register(GvFederation)
class GvFederationAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'gvFederationName',
        'gvMetaDataURL',
        'gvStatus',
        'gvSource',
    )
    list_display = ['gvFederationName', 'gvMetaDataURL', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )

    def has_add_permission(self, request):
        return False

