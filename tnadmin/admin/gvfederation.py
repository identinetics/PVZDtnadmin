from django import forms
from django.contrib import admin
from tnadmin.models.gvfederation import *


@admin.register(GvFederation)
class GvFederationAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'gvfederationname',
        'gvmetadataurl',
        'gvStatus',
        'gvSource',
    )
    list_display = ['gvfederationname', 'gvmetadataurl', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )

    def has_add_permission(self, request):
        return False

    # Make model change-only. Initial insert by migration
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

