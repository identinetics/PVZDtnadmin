from django.contrib.auth.middleware import RemoteUserMiddleware

class CustomRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_PVP_USERID'
