from django import forms
from django.contrib import admin
from fedop.models.userprivilege import *


@admin.register(Userprivilege)
class UserprivilegeAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['subject_cn', 'org_cn', 'not_after']
    #readonly_fields = ('cn', 'cert')
    #search_fields = (
    #    'fqdn',
    #    'org_cn',
    #)

