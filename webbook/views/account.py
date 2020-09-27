from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.views import View

from ..models import account_activation_token
from ..forms import PublicUserForm, SignUpForm
from ..views import User

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
        p_form = PublicUserForm()
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        p_form = PublicUserForm(request.POST)
        if p_form.is_valid():
            user = p_form.save()
            return redirect('/')
        return render(request, self.template_name, locals())

# -----------------------------
class SignupView(View):
    """
        Authentification view
    """
    template_name = "account/signup.html"

    def get(self, request, *args, **kwargs):
        p_form = SignUpForm()
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        p_form = SignUpForm(request.POST)
        if p_form.is_valid():
            user = p_form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, locals())

# -----------------------------
def activation(request, uidb64, token):
    """
        Access to activate an account from email received
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
    except:
        return HttpResponse(status=404)

    try:
        l_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse(status=404)
    else:
        if account_activation_token.check_token(l_user, token):
            l_user.is_active = True
            l_user.save()
            login(request, l_user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return HttpResponse(status=404)
