from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from ..models import User, ActivationEmail
from django.contrib.auth.forms import UserCreationForm

from django.core.mail import send_mail

import logging
logger = logging.getLogger("forms")

class PublicUserForm(forms.ModelForm):
    '''
    This form will be use by User of website to create/update an account
    '''
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password', 'first_name', 'last_name', 'company' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].required = True

class AdminUserForm(forms.ModelForm):
    '''
    This form will be use by Admin of website to create/update an account
    '''
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password', 'first_name', 'last_name', 'is_superuser' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        l_user = super(AdminUserForm, self).save(commit=False)
        l_user.is_staff = True
        l_user.is_active = True
        l_user.save()
        return l_user

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'last_name', 'first_name', 'company' ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label
        self.fields['last_name'].widget.attrs['placeholder'] = self.fields['last_name'].label
        self.fields['first_name'].widget.attrs['placeholder'] = self.fields['first_name'].label
        self.fields['company'].widget.attrs['placeholder'] = self.fields['company'].label

    def save(self, *args, **kwargs):
        l_user = super(SignUpForm, self).save(commit=False)
        l_user.is_staff = False
        l_user.is_active = False
        l_user.is_superuser = False
        l_user.save()
        l_act_email = ActivationEmail.objects.get_or_create(pk=0)
        try:
            send_mail(
                subject=l_act_email.subject,
                message=l_act_email.message,
                recipient_list=[l_user.email],
                fail_silently=False)
        except:
            return None
        return l_user
