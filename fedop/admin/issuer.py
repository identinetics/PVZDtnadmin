from django import forms
from django.contrib import admin
from fedop.models.issuer import *


@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['subject_cn', 'pvprole']
