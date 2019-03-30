from rest_framework import serializers
from portaladmin.models.MDstatement import MDstatement


class MDstatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MDstatement
        fields = (
            'id',
            'admin_note',
            'content_valid',
            'created_at',
            'deletionRequest',
            'ed_file_upload',
            'ed_signed',
            'ed_uploaded',
            'ed_uploaded_filename',
            'entity_fqdn',
            'entityID',
            'make_blank_entityid_unique',
            'namespace',
            'operation',
            'org_cn',
            'org_id',
            'signer_authorized',
            'signer_subject',
            'status',
            'statusgroup',
            'updated_at',
            'validation_message',
        )

