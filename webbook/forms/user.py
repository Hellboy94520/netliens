from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from ..models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from django.core.exceptions import ValidationError

import logging
logger = logging.getLogger("forms")

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

    def send_mail(self,
                  subject_template_name,
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

    def save(self, 
             use_https=False,
             site_domain=None,
             site_name=None,
             email_template_name=None,
             subject_template_name=None,
             from_email=None):
        """
            Generate a one-use only link to validate account creation.
        """
        # Create user without commit
        l_user = super(SignUpForm, self).save(commit=False)
        l_user.is_staff = False
        l_user.is_active = False
        l_user.is_superuser = False
        l_user.save()
        # Set content for email
        context = {
                'email': l_user.email,
                'domain': site_domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(l_user.pk)),
                'user': l_user,
                'token': default_token_generator.make_token(l_user),
                'protocol': 'https' if use_https else 'http'
        }
        # - Send email
        self.send_mail(subject_template_name,
                       email_template_name,
                       context,
                       from_email,
                       l_user.email)
        return True
