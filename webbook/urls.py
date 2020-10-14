# https://github.com/django/django/blob/stable/2.2.x/django/

from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from .views import netliens, languages, account, admin

urlpatterns = [
  # NetLiens
  path('', netliens.HomeView.as_view()),
  path('category/<int:category_id>', netliens.CategoryView.as_view()),
  path('announcement/<int:announcement_id>', netliens.AnnouncementView.as_view()),
  # Languages
  path('languages/<str:language>', languages.activation),
  # Account
  path('account/', account.HomeView.as_view()),
  path('account/signup/',
    account.SignupView.as_view(),
    name="signup"),
  path('account/signup/done/',
    TemplateView.as_view(template_name="account/signup_done.html"),
    name="signup_done"),
  path('account/signup/<uidb64>/<token>/',
    account.SignupConfirmation.as_view(),
    name="signup_confirmation"),
  # --> AuthentificationView: https://docs.djangoproject.com/fr/3.1/topics/auth/default/#module-django.contrib.auth.views
  ## View to Login
  path('account/login/',
    auth_views.LoginView.as_view(template_name="account/login.html"),
    name="login"),
  ## View to Logout
  path('account/logout/',
    auth_views.LogoutView.as_view(),
    name="logout"),
  ## TODO: View to change password
  # path('account/password_change'),
  # path('account/password_change/done'),
  ## View to ask to reset passwork via an email
  path('account/password_reset/',
    auth_views.PasswordResetView.as_view(
      template_name='account/password_reset.html',
      success_url='/account/password_reset/done/',
      email_template_name="account/email_password_reset_content.html",
      subject_template_name="account/email_password_reset_subject.txt",
      title=_("Password reset request")),
    name="password_reset"),
  ## View to indicated that an email has been sent to reset password
  path('account/password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(
      template_name='account/password_reset_done.html',
      title=_("Password reset request done")),
    name="password_reset_done"),
  ## View from email link to reset password
  path('account/password_reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
      template_name="account/password_reset_confirm.html",
      title=_("Password reset")),
    name="password_reset_confirm"),
  ## View to indicated password has been reset
  path('account/password_reset/complete/',
    auth_views.PasswordResetConfirmView.as_view(
      template_name="account/password_reset_complete.html",
      title=_("Password reset complete")),
    name="password_reset_complete"),
  # Admin
  path('admin/', admin.HomeView.as_view()),
]
