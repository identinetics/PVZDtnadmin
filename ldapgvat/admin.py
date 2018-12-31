from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from ldapgvat.models import GvOrganisation

@admin.register(GvOrganisation)
class GvOrganisationAdmin(admin.ModelAdmin):
    exclude = ['dn']
    list_display = ['gvOuId', 'cn']
    search_fields = ['gvOuId', 'cn', 'o']
