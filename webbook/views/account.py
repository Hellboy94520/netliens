from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm
# from django.utils.encoding import force_bytes, force_text
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.views import View

from ..forms import PublicUserForm, SignUpForm

# -----------------------------
# Token
# -----------------------------
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

# -----------------------------
# View
# -----------------------------
@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'account/home.html'

    def get(self, request, *args, **kwargs):
        p_form = PublicUserForm()
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        p_form = PublicUserForm(request.POST)
        if p_form.is_valid():
            user = p_form.save()
            #TODO: Send email
            # print(f"Uid='{urlsafe_base64_encode(force_bytes(user.pk))}'")
            # print(f"Token='{account_activation_token.make_token(user)}'")
            return redirect('/')
        return render(request, self.template_name, locals())

# -----------------------------
class SignupView(View):
    template_name = "account/signup.html"

    def get(self, request, *args, **kwargs):
        p_form = SignUpForm()
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        p_form = SignUpForm(request.POST)
        if p_form.is_valid():
            user = p_form.save()
            #TODO: Send email
            # print(f"Uid='{urlsafe_base64_encode(force_bytes(user.pk))}'")
            # print(f"Token='{account_activation_token.make_token(user)}'")
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, locals())

# -----------------------------
def activation(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    try:
        l_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        #TODO: Write template to contact administration in case of problem or to resend an email
        return HttpResponse('Activation link is invalid!')
    else:
        if account_activation_token.check_token(user, token):
            l_user.is_active = True
            l_user.save()
            login(request, l_user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        #TODO: Write template to contact administration in case of problem or to resend an email
        return HttpResponse('Activation link is invalid!')
