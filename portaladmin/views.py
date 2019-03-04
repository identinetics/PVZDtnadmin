from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from portaladmin.models import MDstatement
from portaladmin.serializers import MDstatementSerializer


class MDstatementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MDstatement.objects.all()
    serializer_class = MDstatementSerializer

