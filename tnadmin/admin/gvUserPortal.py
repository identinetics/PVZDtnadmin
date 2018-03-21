from django import forms
from django.contrib import admin
from tnadmin.models.gvUserPortal import *

@admin.register(GvUserPortal)
class GvUserPortalAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'cn',
        'gvOuIdOwner',
        'gvOuIdParticipant',
        'gvFederationNames',
        'gvSamlIdpEntityId',
        'gvMaxSecClass',
        'description',
        'gvStatus',
        'gvSource',
    )
    list_display = ['cn', 'gvOuIdOwner', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )


@admin.register(GvUserPortalFederationInfo)
class GvUserPortalFederationInfoAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'gvFederationName',
        'gvUserPortal',
        'gvStatus',
        'gvSource',
    )
    list_display = ['gvFederationName', 'gvUserPortal', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )
