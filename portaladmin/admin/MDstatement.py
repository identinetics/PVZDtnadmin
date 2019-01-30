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
from .mds_sign_and_update import mds_sign_and_update
from ..constants import *
from ..exceptions import CancelRequest
from ..models import MDstatement
from ..signals import md_statement_edit_starts
# from PVZDpy.cresignedxml import creSignedXML
# from PVZDpy.samlentitydescriptor import SAMLEntityDescriptorFromStrFactory, SAMLEntityDescriptor

from PVZDpy.cresignedxml import get_seclay_requesttemplate


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
        md_namespace_prefix = 'md'  # FIXME
        template = get_seclay_requesttemplate(sigType='enveloped',
                                              sigPosition='/' + md_namespace_prefix + ':EntityDescriptor')
        # TODO use file if needed
        xml = template % MDstatement.objects.get(id=id).ed_uploaded
        # TODO 404

        return HttpResponse(xml, content_type='text/xml')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        md_statement = MDstatement.objects.get(id=object_id)

        extra_context['ed_uploaded_get_template_url'] = reverse('admin:portaladmin_get_signature_request',
                                                            args=[md_statement.id])

        return super().change_view(request, object_id, form_url, extra_context)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #
    #     extra_context = extra_context or {}
    #
    #     # don't work due:
    #     # https://github.com/django/django/blob/master/django/contrib/admin/templatetags/admin_modify.py#L73
    #     # extra_context['show_save_and_continue'] = False
    #     # extra_context['show_save_and_add_another'] = False
    #
    #     delta_min = getattr(settings, 'PORTALADMIN_CHECKOUT_MINUTES', 15)
    #     datetime_ago = timezone.now() - timedelta(minutes=delta_min)
    #
    #     try:
    #         md_statement = MDstatement.objects.get(id=object_id)
    #     except MDstatement.DoesNotExist:
    #         raise Http404("Metadaten Statement does not exist")  # TODO translate
    #
    #     if md_statement.checkout_status:
    #         # CheckOut by another user
    #         if md_statement.checkout_status.checkout_by != request.user \
    #                 and md_statement.checkout_status.created_at > datetime_ago:
    #             # we need to create custom error page or disable UI of admin form
    #             assert False, 'The Metadata Statement is locked by another user, please try again later'
    #
    #     md_statement_edit_starts.send(sender=MDstatement, md_statement=md_statement, current_user=request.user)
    #
    #     return super().change_view(request, object_id, form_url, extra_context)

    actions = ['delete_selected', 'sign_and_update_action']  # for dev
    #actions = ['sign_and_update_action']

    def sign_and_update_action(self, request, queryset):
        try:
            mds_sign_and_update(self, request, queryset)
            messages.info(request, "EntityDescriptor signiert")
        except CancelRequest:
            pass
        except(Exception) as e:
            messages.error(request, str(e))
    sign_and_update_action.short_description = "EntityDescriptor mit lokaler BKU signieren"

    def get_action_choices(self, request):
        # remove default blank selection in action drop-down
        choices = super(MDstatementAdmin, self).get_action_choices(request)
        choices.pop(0) # choices is a list, the first is the BLANK_CHOICE_DASH
        return choices
