from django import forms
from django.contrib import admin
from portaladmin.models.MDstatement import *


@admin.register(MDstatement)
class MDstatementAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['entityID', 'Status']
    readonly_fields = list_display
    search_fields = ('entityID', 'Status', )
