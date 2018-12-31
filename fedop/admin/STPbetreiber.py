from django import forms
from django.contrib import admin
from fedop.models.STPbetreiber import *


@admin.register(STPbetreiber)
class STPbetreiberAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['gvOuId', 'cn']
    #readonly_fields = ('gvSource', 'cn')
    #search_fields = (
    #    'gvOuId',
    #)
