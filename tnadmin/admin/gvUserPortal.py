from django import forms
from django.contrib import admin
from tnadmin.models.gvUserPortal import *

@admin.register(gvUserPortal)
class gvUserPortalAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'cn',
        'gvOuIdOwner',
        'gvMaxSecClass',
        'description',
        'gvStatus',
        'gvSource',
    )
    list_display = ['cn', 'gvOuIdOwner', 'gvStatus', 'gvSource']
    readonly_fields = ('gvSource', )
