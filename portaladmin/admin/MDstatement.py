from django import forms
from django.contrib import admin
from portaladmin.models.MDstatement import *


@admin.register(MDstatement)
class MDstatementAdmin(admin.ModelAdmin):
    actions = None
    #list_display = ['fqdn', 'org_cn']
    #readonly_fields = ('fqdn', 'org_cn')
    #search_fields = (
    #    'fqdn',
    #    'org_cn',
    #)

    #def org_cn(self):
    #    return self.gvOuIdParent.cn