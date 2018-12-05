from django import forms
from django.contrib import admin
from fedop.models.revocation import Revocation


@admin.register(Revocation)
class RevocationAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['subject_cn', 'cert']
