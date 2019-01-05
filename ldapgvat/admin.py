from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from ldapgvat.models import GvOrganisation

@admin.register(GvOrganisation)
class GvOrganisationAdmin(admin.ModelAdmin):
    exclude = ['dn']
    list_display = ['gvouid', 'cn']
    search_fields = ['gvouid', 'cn', 'o']
