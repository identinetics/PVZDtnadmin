from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from tnadmin.models.ldapsync import *

@admin.register(LdapSyncJobPull)
class LdapSyncJobPullAdmin(admin.ModelAdmin):
    actions = None
    fields = (
        'started_at',
        'add_upd_records_update_failed',
    )

    list_display = fields + ('link_to_detail', )
#    #list_display_links = ['o' ]
    readonly_fields = list_display
    search_fields = list_display

    def link_to_detail(self, obj: LdapSyncJobPull):
        #link = reverse("admin:tnadmin_model_change", args=[obj.id])
        return format_html(f'<a href="/admin/tnadmin/ldapsyncerrorpull/?job_id__id__exact={obj.id}">{obj.id} (details)</a>')

    link_to_detail.allow_tags=True
    link_to_detail.short_description = 'List errors'
    link_to_detail.admin_order_field = 'errors'  # Make row sortable


@admin.register(LdapSyncErrorPull)
class LdapSyncErrorPullAdmin(admin.ModelAdmin):
    actions = None
    list_display = (
        'ldap_dn',
        'op',
        'message',
        'job_id',
    )
    # list_display_links = ['o' ]
    readonly_fields = list_display
    list_filter = ('job_id', 'op')
    search_fields = ( 'op', 'ldap_dn',)

