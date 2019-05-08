from django.contrib.auth.models import Group
from django.contrib.auth.backends import RemoteUserBackend

class CustomRemoteUserBackend(RemoteUserBackend):
    """ Make new users staff and assign all groups """

    def configure_user(self, request, user):
        """ Configure user after creation and returns the updated user. """

        user.is_staff = True
        user.is_superuser = False
        user.first_name = request.META.get('HTTP_PVP_GIVEN_NAME', '')
        user.last_name = request.META.get('HTTP_PVP_LAST_NAME', '')
        user.email = request.META.get('HTTP_PVP_MAIL', '')
        all_groups = Group.objects.all()
        user.groups.set(all_groups)
        user.save()
        return user