from django import forms
from django.contrib import admin
from tnadmin.models.gvOrg import *
from tnadmin.models.gvFederationOrg import *




@admin.register(GvFederationOrg)
class GvFederationOrgAdmin(admin.ModelAdmin):
    actions = None
    autocomplete_fields = ('gvOuId', 'gvCaseOrg', 'gvOuId2', 'gvOuId3')
    fields = (
        'gvOuId',
        'gvOuId2',
        'gvOuId3',
        'gvContractStatus',
        'gvDateEffective',
        'gvDateTerminated',
        'gvCaseOrg',
        'gvCaseNumber',
        'description',
        'gvStatus',
        'gvSource',
    )
    list_display = ('gvOuId', 'get_org_o', 'gvContractStatus', 'get_org_o2', 'gvStatus', 'gvSource')
    readonly_fields = ('gvSource', )
    search_fields = (
        'gvOuId',
        'gvContractStatus',
        'gvDateEffective',
        'gvDateTerminated',
        'gvCaseOrg',
        'gvStatus',
        'gvSource',
    )

    def get_org_o(self, inst):
        return inst.gvOuId.o
    get_org_o.short_description = 'Kurzbezeichnung'

    def get_org_o2(self, inst):
        if inst.gvOuId2 is not None:
            return "%s (%s)" % (inst.gvOuId2, inst.gvOuId2.o)
        else:
            return ''
    get_org_o2.short_description = 'Vertragspartei (Aufsicht)'

    def get_org_o3(self, inst):
        if inst.gvOuId3 is not None:
            return "%s (%s)" % (inst.gvOuId3, inst.gvOuId3.o)
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

