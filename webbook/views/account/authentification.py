from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.views import View
from django.views.generic import TemplateView


from ..common import decorators as my_decorators

from ...models import User
from ...forms import SignUpForm, send_mail as SendEmail

# -----------------------------
# Token
# -----------------------------
from django.utils.http import urlsafe_base64_decode

# -----------------------------
@method_decorator(my_decorators.logout_required, name='dispatch')
class SignupView(View):
    """
        View to create an account
    """
    form_class = SignUpForm
    template_name = 'account/signup.html'
    success_url = "/account/signup/done/"
    email_template_name = "account/email_signup_content.html"
    subject_template_name = "account/email_signup_subject.txt"
    from_email = None
    title = _('Signup')

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            opts = {
            'use_https': request.is_secure(),
            'site_domain': current_site.domain,
            'site_name': current_site.name,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'from_email': self.from_email
            }
            form.save(**opts)
            return redirect(self.success_url)
        return render(request, self.template_name, locals())

# -----------------------------
class SignupConfirmation(TemplateView):
    """
        View to activate account
    """
    template_name = None
    email_template_name = None
    subject_template_name = None

    def get_user(self, uidb64):
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        l_user = get_object_or_404(User, pk=uid)
        return l_user

    def get(self, request, *args, **kwargs):
        # - Activate account
        assert 'uidb64' in kwargs and 'token' in kwargs, Http404()
        l_user = self.get_user(kwargs['uidb64'])
        if not default_token_generator.check_token(l_user, kwargs['token']):
            raise Http404()
        l_user.is_active = True
        l_user.save()
        # - Send Email
        opts = {
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'context': { 'user': l_user },
            'from_email': None,
            'to_email': l_user.email
        }
        SendEmail(**opts)
        login(request, l_user)
        return super(SignupConfirmation, self).get(request, *args, **kwargs)


# -----------------------------
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from ...forms import PasswordChangeForm
class PasswordChangeView(DjangoPasswordChangeView):
    """
        View to request Password change
    """
    email_template_name = None
    subject_template_name = None
    form_class = PasswordChangeForm

    def form_valid(self, form):
        l_view = super(DjangoPasswordChangeView, self).form_valid(form)
        opts = {
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'from_email': None,
            'to_email': form.user.email
        }
        form.send_email(**opts)
        return l_view


# -----------------------------
from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
from ...forms import SetPasswordForm
class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    """
        View to update Password from Email
    """
    email_template_name = None
    subject_template_name = None
    form_class = SetPasswordForm
    # Seems to not work with my form_valid:
    post_reset_login = True

    def form_valid(self, form):
        l_view = super(DjangoPasswordResetConfirmView, self).form_valid(form)
        opts = {
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'from_email': None,
            'to_email': form.user.email
        }
        form.send_email(**opts)
        return l_view

