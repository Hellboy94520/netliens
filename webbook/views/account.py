from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from ..models import User
from ..forms import PublicUserForm, SignUpForm

#TODO: To delete when ErrorPages will be implement when activation link is incorrect
from django.http import HttpResponse

# -----------------------------
# Token
# -----------------------------
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode

# -----------------------------
# View
# -----------------------------
@method_decorator(login_required, name='dispatch')
class HomeView(View):
    """
        View to update account
    """
    template_name = 'account/home.html'

    def get(self, request, *args, **kwargs):
        form = PublicUserForm(instance=request.user)
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        form = PublicUserForm(request.POST,
                                instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('/')
        return render(request, self.template_name, locals())

# -----------------------------
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
    template_name = "account/signup_confirmation.html"

    def get_user(self, uidb64):
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        l_user = get_object_or_404(User, pk=uid)
        return l_user

    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs, Http404()
        l_user = self.get_user(kwargs['uidb64'])
        if not default_token_generator.check_token(l_user, kwargs['token']):
            raise Http404()
        l_user.is_active = True
        l_user.save()
        return super(SignupConfirmation, self).get(request, *args, **kwargs)
