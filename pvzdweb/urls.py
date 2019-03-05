"""PVZDweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
import portaladmin.views
from portaladmin.views import MDstatementViewSet


# disable access control
class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s,*a,**kw: True

admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True

router = routers.DefaultRouter()
router.register(r'mdstatement', MDstatementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fedop/', include('fedop.urls')),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='PVZD API')),
    re_path('api/unsignedxml/(?P<id>\d+)/', portaladmin.views.unsignedxml),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # if it will not debug then we can use web server config to delivery of media files

# add static files app level for dev
from django.contrib.staticfiles import views
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]

admin.site.site_header = 'PVZD Teilnehmerverwaltung'
admin.site.index_title = 'Features area'
admin.site.site_title = 'HTML title from adminsitration'