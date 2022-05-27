# https://github.com/django/django/blob/stable/2.2.x/django/

from django.urls import path, include, re_path
from django.contrib import admin
from webbook.views.account.authentification import CategoryView

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
# router = routers.DefaultRouter()
# router.register(r'todos', views.TodoView, 'todo')
router = routers.SimpleRouter()
router.register('category', CategoryView, 'newcategory')
urlpatterns = [
  re_path(r'^api/', include((router.urls))),
  path('api/token/', TokenObtainPairView.as_view()),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
# urlpatterns = [
#   path('admin/', admin.site.urls),
#   path('', include(router.urls)),
  # NetLiens
  # path('', netliens.HomeView.as_view()),
  # path('category/<int:category_id>', netliens.CategoryView.as_view()),
  # path('announcement/<str:announcement_url>', netliens.AnnouncementView.as_view()),
  # # Languages
  # path('languages/<str:language>', languages.activation),
  # # ------------------------------------------------------------------------
  # # Account
  # # # --> AuthentificationView: https://docs.djangoproject.com/fr/3.1/topics/auth/default/#module-django.contrib.auth.views
  # # ------------------------------------------------------------------------
  # path('account/',
  #   account.home.HomeView.as_view(template_name="account/home.html"),
  #   name="account"),
  # path('account/signup/',
  #   account.authentification.SignupView.as_view(),
  #   name="signup"),
  # path('account/signup/done/',
  #   TemplateView.as_view(template_name="account/signup_done.html"),
  #   name="signup_done"),
  # path('account/signup/<uidb64>/<token>/',
  #   account.authentification.SignupConfirmation.as_view(
  #     template_name="account/signup_confirmation.html",
  #     email_template_name="account/email_signup_confirmation_content.html",
  #     subject_template_name="account/email_signup_confirmation_subject.txt"
  #   ),
  #   name="signup_confirmation"),
  # path('account/login/',
  #   auth_views.LoginView.as_view(template_name="account/login.html"),
  #   name="login"),
  # path('account/logout/',
  #   auth_views.LogoutView.as_view(),
  #   name="logout"),
  # path('account/password_change/',
  #   account.authentification.PasswordChangeView.as_view(
  #     template_name="account/password_change.html",
  #     success_url="/account/password_change/done",
  #     email_template_name="account/email_password_change_content.html",
  #     subject_template_name="account/email_password_change_subject.txt"
  #   )),
  # path('account/password_change/done/',
  #   auth_views.PasswordChangeDoneView.as_view(
  #     template_name="account/password_change_done.html"
  #   )),
  # path('account/password_reset/',
  #   auth_views.PasswordResetView.as_view(
  #     template_name='account/password_reset.html',
  #     success_url='/account/password_reset/done/',
  #     email_template_name="account/email_password_reset_content.html",
  #     subject_template_name="account/email_password_reset_subject.txt",
  #     title=_("Password reset request")),
  #   name="password_reset"),
  # path('account/password_reset/done/',
  #   auth_views.PasswordResetDoneView.as_view(
  #     template_name='account/password_reset_done.html',
  #     title=_("Password reset request done")),
  #   name="password_reset_done"),
  # path('account/password_reset/<uidb64>/<token>/',
  #   account.authentification.PasswordResetConfirmView.as_view(
  #     template_name="account/password_reset_confirm.html",
  #     email_template_name="account/email_password_reset_confirm_content.html",
  #     subject_template_name="account/email_password_reset_confirm_subject.txt",
  #     title=_("Password reset")),
  #   name="password_reset_confirm"),
  # path('account/password_reset/complete/',
  #   auth_views.PasswordResetCompleteView.as_view(
  #     template_name="account/password_reset_complete.html",
  #     title=_("Password reset complete")),
  #   name="password_reset_complete"),
  # path('account/deletion/',
  #   account.authentification.DeleteView.as_view(
  #     template_name="account/account_deletion.html",
  #     success_url="/account/deletion/done/",
  #     email_context_deletion_url="account/deletion/<uidb64>/<token>/complete/",
  #     email_template_name="account/email_deletion_content.html",
  #     subject_template_name="account/email_deletion_subject.txt"),
  #   name="account_deletion"),
  # path('account/deletion/done/',
  #   TemplateView.as_view(
  #     template_name='account/account_deletion_done.html'),
  #   name="account_deletion_done"),
  # path('account/deletion/<uidb64>/<token>/complete/',
  #   account.authentification.DeleteCompleteView.as_view(
  #     template_name="account/account_deletion_complete.html",
  #     success_url="/",
  #     cancel_url="account/",
  #     email_template_name="account/email_deletion_complete_content.html",
  #     subject_template_name="account/email_deletion_coomplete_subject.txt"),
  #   name="account_deletion_complete"
  #   ),
  # #   name="account_deletion_complete"),
  # # path('account/update/', account.UpdateView.as_view(template_name="account/update.html"),
  # #   name="account_update"),
  # # path('account/delete/', account.)
  # # path('account/announcement/', account.AnnouncementView.as_view(template_name="account/announcement.html"),
  # #   name="account_announcement"),
  # # path('account/announcement/creation/', account.AnnouncementCreationView.as_view(
  # #     template_name="account/announcement_creation.html",
  # #     success_url="/account/announcement/<str:announcement_url>/"),
  # #   name="account_announcement_creation"),
  # # path('account/announcement/<str:announcement_url>/', account.AnnouncementDataView.as_view(
  # #     template_name="account/accouncement_data.html",
  # #     success_url="/account/announcement/"),
  # #   name="account_announcement_creation_data"),
  # # path('account/announcement/update/<str:announcement_url>/', account.AnnouncementUpdateView.as_view(
  # #     template_name="account/announcement_update.html",
  # #     success_url=""),
  # #   name="account_announcement_update"),
  # # path('account/announcement/purchase/', account.AnnouncementPurchaseView.as_view(
  # #     template_name="account/announcement_purchase.html")),

  # Admin
  # path('admin/', admin.HomeView.as_view(
  #     template_name="admin/homepage.html")),
  # path('admin/category', admin.CategoryView.as_view(
  #     template_name="admin/category.html")),
  # path('admin/localisation', admin.LocalisationView.as_view(
  #     template_name="admin/localisation.html")),
# ]
