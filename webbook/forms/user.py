from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from ..models import User
from django.contrib.auth.forms import UserCreationForm

import logging
logger = logging.getLogger("forms")

def send_mail(subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email):
    """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    email_message.send()

# -----------------------------
# Form
# -----------------------------
class PublicUserForm(forms.ModelForm):
    """
        This form is used by User of website to create/update an account
    """
    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'last_name', 'company' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].required = True

# -----------------------------
class AdminUserForm(forms.ModelForm):
    """
        This form is used by Admin of website to create/update an account
    """
    class Meta:
        model = User
        fields = '__all__'

# -----------------------------
class SignUpForm(UserCreationForm):
    """
        This form is used to create an account
    """
    class Meta:
        model = User
        fields = [ 'email', 'last_name', 'first_name', 'company' ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label
        self.fields['last_name'].widget.attrs['placeholder'] = self.fields['last_name'].label
        self.fields['first_name'].widget.attrs['placeholder'] = self.fields['first_name'].label
        self.fields['company'].widget.attrs['placeholder'] = self.fields['company'].label

    def save(self):
        """
            Generate a one-use only link to validate account creation.
        """
        # Create user without commit
        self.user = super(SignUpForm, self).save(commit=False)
        self.user.is_staff = False
        self.user.is_active = False
        self.user.is_superuser = False
        self.user.save()
        return True

class CheckPasswordForm(forms.Form):
    """
        This form is used to identify the user
    """
    password = forms.CharField(
        required=True,
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(),
    )

    def is_valid(self, user):
        if not super(CheckPasswordForm, self).is_valid():
            return False
        if not user.check_password(self.cleaned_data['password']):
            self.add_error('password', _("Invalid Password !"))
            return False
        return True
