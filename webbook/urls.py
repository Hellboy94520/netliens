from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

from .views import netliens, languages

from django.contrib.auth.decorators import permission_required

urlpatterns = [
  # NetLiens
  path('', netliens.home, name='home'),
  # Languages
  path('languages/<str:language>', languages.activation)
]
