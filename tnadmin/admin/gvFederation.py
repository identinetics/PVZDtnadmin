from django import forms
from django.contrib import admin
from tnadmin.models.gvFederation import *


@admin.register(GvFederation)
class GvFederationAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'gvFederationName',
        'gvMetaDataURL',
        'gvDefaultFederation',
        'gvOuId',
        'gvStatus',
        'gvSource',
    )
    list_display = ['gvFederationName', 'get_federationoperator', 'gvMetaDataURL', 'gvDefaultFederation', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )

    def get_federationoperator(self, inst):
        return inst.gvOuId.o
    get_federationoperator.short_description = 'Depositar/FO'

