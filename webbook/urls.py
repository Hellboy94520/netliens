from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

from .views import netliens, languages, account

from django.contrib.auth.decorators import permission_required


urlpatterns = [
  # NetLiens
  path('', netliens.home, name='home'),
  # Languages
  path('languages/<str:language>', languages.activation),
  # Account
  path('account/', account.HomeView.as_view()),
  path('account/login/', auth_views.LoginView.as_view(template_name='account/login.html')),
  path('account/logout/', auth_views.LogoutView.as_view()),
  path('account/signup/', account.SignupView.as_view()),
  url(r'^account/activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', account.activation, name='activate'),
]
