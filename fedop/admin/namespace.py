from django import forms
from django.contrib import admin
from fedop.models.namespace import *


@admin.register(Namespaceobj)
class NamespaceobjAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['fqdn', 'get_gvouid', 'org_cn']
    #readonly_fields = ('fqdn', 'org_cn')
    search_fields = (
        'fqdn',
    )

    def get_gvouid(self, obj):
        return obj.gvouid_parent.gvouid.gvouid
    get_gvouid.short_description = 'gvouid'