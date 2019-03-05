from rest_framework import viewsets
from portaladmin.models import MDstatement
from portaladmin.serializers import MDstatementSerializer
from django.views.decorators.cache import never_cache

# @never_cache  TODO: make this working with CBV
class MDstatementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MDstatement.objects.all()
    serializer_class = MDstatementSerializer

