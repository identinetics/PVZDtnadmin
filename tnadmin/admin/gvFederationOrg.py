from django import forms
from django.contrib import admin
from tnadmin.models.gvorg import *
from tnadmin.models.gvFederationOrg import *




@admin.register(GvFederationOrg)
class GvFederationOrgAdmin(admin.ModelAdmin):
    #actions = None
    autocomplete_fields = ('gvouid', 'gvCaseOrg', 'gvouid_aufsicht', 'gvouid_dl')
    fields = (
        'gvouid',
        'gvouid_aufsicht',
        'gvouid_dl',
        'gvContractStatus',
        'gvDateEffective',
        'gvDateTerminated',
        'gvCaseOrg',
        'gvCaseNumber',
        'description',
        'gvStatus',
        'gvSource',
    )
    list_display = ('gvouid', 'get_org_o', 'gvContractStatus', 'get_org_o2', 'gvStatus', 'gvSource')
    readonly_fields = ('gvSource', )
    list_filter = (
        'gvContractStatus',
        'gvStatus',
    )
    search_fields = (
        'gvouid',
        'gvContractStatus',
        'gvDateEffective',
        'gvDateTerminated',
        'gvCaseOrg',
        'gvStatus',
        'gvSource',
    )

    def get_org_o(self, inst):
        return inst.gvouid.o
    get_org_o.short_description = 'Kurzbezeichnung'

    def get_org_o2(self, inst):
        if inst.gvouid_aufsicht is not None:
            return "%s (%s)" % (inst.gvouid_aufsicht, inst.gvouid_aufsicht.o)
        else:
            return ''
    get_org_o2.short_description = 'Vertragspartei (Aufsicht)'

    def get_org_o3(self, inst):
        if inst.gvouid_dl is not None:
            return "%s (%s)" % (inst.gvouid_dl, inst.gvouid_dl.o)
        else:
            return ''
    get_org_o3.short_description = 'Dienstleister'

    def get_query_set(self):
        return super(Requirement, self).get_query_set().select_related('GvOrganisation', )  # improve performance by joining related tables

@admin.register(GvParticipant)
class GvParticipant(GvFederationOrgAdmin):
    pass

@admin.register(GvUserPortalOperator)
class GvUserPortalOperator(GvFederationOrgAdmin):
    pass

