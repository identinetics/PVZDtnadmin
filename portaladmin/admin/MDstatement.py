from datetime import timedelta

from django import forms
from django.urls import path, reverse
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
from django.http import Http404
from django.db import models
from django.forms.widgets import ClearableFileInput
from ..constants import *
from ..exceptions import CancelRequest
from ..models import MDstatement
from PVZDpy.samlentitydescriptor import SAMLEntityDescriptor

from PVZDpy.get_seclay_request import get_seclay_request


class FileInputWidget(ClearableFileInput):
    template_name = 'portaladmin/widgets/clearable_file_input.html'


class MDstatementForm(forms.ModelForm):

    class Meta:
        model = MDstatement
        exclude = ['checkout_status']

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.ed_uploaded:
            if not cleaned_data.get("ed_file_upload"):
                self.add_error('ed_file_upload', 'Es wurde noch kein EntityDescriptor hochgeladen')


site.disable_action('delete_selected')


@admin.register(MDstatement)
class MDstatementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.FileField: {'widget': FileInputWidget},
    }
    change_form_template = "portaladmin/md_statement_admin_change_form.html"
    form = MDstatementForm
    save_on_top = True
    readonly_fields = (
        'content_valid',
        'created_at',
        'ed_signed',
        'ed_uploaded',
        'ed_uploaded_filename',
        'entityID',
        'get_boilerplate_help',
        'signer_subject',
        'namespace',
        'operation',
        'org_cn',
        'org_id',
        'signer_authorized',
        'status',
        'updated_at',
        'validation_message',
    )
    list_display = (
        'entity_fqdn',
        'status',
        'content_valid',
        'signer_authorized',
        'operation',
        'namespace',
        'org_id',
        'signer_subject',
        'get_validation_message_trunc',
        'updated',
        'admin_note',
    )
    list_display_links = ('entity_fqdn', 'status')
    list_filter = (
        'status',
        'namespace',
        'org_id',
        'signer_subject',
    )
    search_fields = (
        'entity_fqdn',
        'status',
        'operation',
        'namespace',
        'org_id',
        'signer_subject',
        'admin_note',
    )
    fieldsets = (
        (None, {
            'fields': ('get_boilerplate_help', )
        }),
        ('Entity', {
            'fields': (
                'entityID',
                'operation',
            )
        }),
        ('Datei hochladen', {
            'fields': (
                'ed_file_upload',
                'ed_uploaded_filename',
            )
        }),
        ('Prozess Status', {
            'fields': (
                'status',
                'content_valid',
                'signer_authorized',
                'validation_message',
            )
        }),
        ('Adminsitrative Attribute', {
            'fields': (
                ('created_at', 'updated_at', ),
                'signer_subject',
                'admin_note',
            )
        }),
        ('EntityDescriptor XML', {
            'classes': ('collapse',),
            'fields': ('ed_uploaded', 'ed_signed', ),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_signature_request/<int:id>/request.xml',
                 self.get_signature_request_view,
                 name='portaladmin_get_signature_request'),
        ]
        return custom_urls + urls

    def get_signature_request_view(self, request, id):
        ed_str = MDstatement.objects.get(id=id).ed_uploaded
        md_namespace_prefix = SAMLEntityDescriptor.get_namespace_prefix(ed_str)
        sig_pos = '/' + md_namespace_prefix + ':EntityDescriptor'
        xml = get_seclay_request('enveloped', ed_str, sigPosition=sig_pos)
        return HttpResponse(xml, content_type='text/xml')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        md_statement = MDstatement.objects.get(id=object_id)

        extra_context['ed_uploaded_get_template_url'] = reverse('admin:portaladmin_get_signature_request',
                                                            args=[md_statement.id])

        return super().change_view(request, object_id, form_url, extra_context)

    actions = ['delete_selected', ]  # for dev
    #actions = []

