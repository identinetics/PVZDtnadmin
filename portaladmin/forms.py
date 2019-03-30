from django.core.exceptions import ValidationError
from django.forms import ModelForm
from portaladmin.models.MDstatement import MDstatement
from portaladmin.constants import STATUS_ACCEPTED, STATUS_REQUEST_QUEUE, STATUS_SIGNATURE_APPLIED, STATUS_UPLOADED

class MDstatementForm(ModelForm):

    class Meta:
        model = MDstatement
        exclude = []

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.ed_uploaded:
            if not cleaned_data.get("ed_file_upload"):
                self.add_error('ed_file_upload', 'Es wurde noch kein EntityDescriptor hochgeladen')
        if 'Sign' in self.data:
            try:
                mds = MDstatement.objects.get(id=self.instance.id)
            except Exception as e:
                raise ValidationError('Signatur kann nicht erstellt werden bevor die Eingabe gesichert wird.')

            if mds.status in (STATUS_REQUEST_QUEUE, STATUS_SIGNATURE_APPLIED, STATUS_ACCEPTED):
                raise ValidationError("EntityDescriptor wurde bereits signiert")
            if mds.status != STATUS_UPLOADED:
                raise ValidationError("Vor dem Signieren muss ein neuer Entityescriptor hochgeladen werden")
            if not mds.content_valid:
                raise ValidationError("Nur ein gültiger EntityDescriptor kann signiert werden")

