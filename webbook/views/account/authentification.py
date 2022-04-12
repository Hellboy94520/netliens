import json
from django.forms.forms import Form
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# from django.views import View
# from django.views.generic import TemplateView, FormView

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from webbook.models import NewCategory
from webbook.serializer import NewCategorySerializer

# from ..common import decorators as my_decorators
# from ..common import email

class CategoryView(ModelViewSet):

    serializer_class = NewCategorySerializer
    queryset = NewCategory.objects.all()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)



# from ...models import User
# from ...forms import CheckPasswordForm, SignUpForm, send_mail as SendEmail

# -----------------------------
# Token
# -----------------------------
# from django.utils.http import urlsafe_base64_decode

# -----------------------------
# @method_decorator(my_decorators.logout_required, name='dispatch')
# class SignupView(View):
#     """
#         View to create an account
#     """
#     form_class = SignUpForm
#     template_name = 'account/signup.html'
#     success_url = "/account/signup/done/"
#     email_template_name = "account/email_signup_content.html"
#     subject_template_name = "account/email_signup_subject.txt"
#     from_email = None
#     title = _('Signup')

#     def get(self, request, *args, **kwargs):
#         form = SignUpForm()
#         return render(request, self.template_name, locals())

#     def post(self, request, *args, **kwargs):
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             context = {
#                 'uid': urlsafe_base64_encode(force_bytes(form.user.pk)),
#                 'user': form.user,
#                 'token': default_token_generator.make_token(form.user),
#             }
#             opts = {
#                 'request': request,
#                 'subject_template_name': self.subject_template_name,
#                 'email_template_name': self.email_template_name,
#                 'context': context,
#                 'to_email': [form.user.email]
#             }
#             email.send_mail(**opts)
#             return redirect(self.success_url)
#         return render(request, self.template_name, locals())

# # -----------------------------
# class SignupConfirmation(TemplateView):
#     """
#         View to activate account
#     """
#     template_name = None
#     email_template_name = None
#     subject_template_name = None

#     def get_user(self, uidb64):
#         # urlsafe_base64_decode() decodes to bytestring
#         uid = urlsafe_base64_decode(uidb64).decode()
#         l_user = get_object_or_404(User, pk=uid)
#         return l_user

#     def get(self, request, *args, **kwargs):
#         # - Activate account
#         assert 'uidb64' in kwargs and 'token' in kwargs, Http404()
#         l_user = self.get_user(kwargs['uidb64'])
#         if not default_token_generator.check_token(l_user, kwargs['token']):
#             raise Http404()
#         l_user.is_active = True
#         l_user.save()
#         # - Send Email
#         context = {
#             'user': l_user
#         }
#         opts = {
#             'request': request,
#             'email_template_name': self.email_template_name,
#             'subject_template_name': self.subject_template_name,
#             'context': context,
#             'to_email': [l_user.email]
#         }
#         email.send_mail(**opts)
#         login(request, l_user)
#         return super(SignupConfirmation, self).get(request, *args, **kwargs)


# # -----------------------------
# from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
# from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
# class PasswordChangeView(DjangoPasswordChangeView):
#     """
#         View to request Password change
#     """
#     email_template_name = None
#     subject_template_name = None
#     form_class = DjangoPasswordChangeForm

#     def post(self, request, *args, **kwargs):
#         form = DjangoPasswordChangeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             opts = {
#                 'request': request,
#                 'subject_template_name': self.subject_template_name,
#                 'email_template_name': self.email_template_name,
#                 'context': None,
#                 'to_email': [form.user.email]
#             }
#             email.send_mail(**opts)
#             return redirect(self.success_url)
#         return render(request, self.template_name, locals())


# # -----------------------------
# from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
# from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
# class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
#     """
#         View to update Password from Email
#     """
#     email_template_name = None
#     subject_template_name = None
#     form_class = DjangoSetPasswordForm
#     post_reset_login = True

#     def post(self, request, *args, **kwargs):
#         form = DjangoPasswordChangeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             opts = {
#                 'request': request,
#                 'subject_template_name': self.subject_template_name,
#                 'email_template_name': self.email_template_name,
#                 'context': None,
#                 'to_email': [form.user.email]
#             }
#             email.send_mail(**opts)
#             return redirect(self.success_url)
#         return render(request, self.template_name, locals())



# @method_decorator(login_required, name='dispatch')
# class DeleteView(FormView):
#     form_class = CheckPasswordForm
#     email_context_deletion_url = None
#     email_template_name = None
#     subject_template_name = None

#     def get(self, request, *args, **kwargs):
#         return super(DeleteView, self).get(request, args, kwargs)

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid(user=request.user):
#             context = {
#                 'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
#                 'user': request.user,
#                 'token': default_token_generator.make_token(request.user),
#             }
#             opts = {
#                 'request': request,
#                 'subject_template_name': self.subject_template_name,
#                 'email_template_name': self.email_template_name,
#                 'context': context,
#                 'to_email': [request.user.email]
#             }
#             email.send_mail(**opts)
#             return redirect(self.success_url)
#         return render(request, self.template_name, locals())

# @method_decorator(login_required, name='dispatch')
# class DeleteCompleteView(TemplateView):
#     success_url = None
#     cancel_url = None
#     email_template_name = None
#     subject_template_name = None

#     #Accessible only via Email
#     #TODO: Template with a confirm/cancel button.
#     def post(self, request, *args, **kwargs):
#         print(request)
#         print(args)
#         print(kwargs)
#         # # Manage Which buttons has been pushed
#         # l_user = User.objects.get(email=request.context['user'])
#         # l_user.is_active=False
#         # l_user.save()
#         # #TODO: What is the behavior, we want here ?
#         # logout()
#         return render(request, self.template_name, locals())
