from django.urls import include, path

from . import views

urlpatterns = [
    path('pjupdate/preview', views.pjupdate, name='pjupdate', kwargs={'mode': 'preview'}),
    path('pjupdate/confirm', views.pjupdate, name='pjupdate', kwargs={'mode': 'confirm'}),
]