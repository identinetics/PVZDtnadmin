from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from tnadmin.models.ldapSync import *

@admin.register(LdapSyncJob)
class LdapSyncJobAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'started_at',
        'add_upd_records_update_failed',
    )

    list_display = fields + ('link_to_detail', )
#    #list_display_links = ['o' ]
    readonly_fields = list_display
    search_fields = list_display

    def link_to_detail(self, obj: LdapSyncJob):
        #link = reverse("admin:tnadmin_model_change", args=[obj.id])
        return mark_safe(f'<a href="">{escape(obj.__str__())}</a>')

    link_to_detail.allow_tags=True
    link_to_detail.short_description = 'List errors'
    link_to_detail.admin_order_field = 'list errors'  # Make row sortable


@admin.register(LdapSyncError)
class LdapSyncErrorAdmin(admin.ModelAdmin):
    actions = None
    list_display = (
        'ldap_dn',
        'op',
        'message',
        'job_id',
    )
    # list_display_links = ['o' ]
    readonly_fields = list_display
    search_fields = list_display

