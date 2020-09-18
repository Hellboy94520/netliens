from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from ..models import User, UserType

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

    # def clean(self):
    #    email = self.cleaned_data.get('email')
    #    if not email:
    #        self.add_error('email', _("This field is required."))
    #    if User.objects.filter(email=email).exists():
    #        self.add_error('email', _("Email already exists !"))
    #    return self.cleaned_data

    # def save(self, *args, **kwargs):
    #     l_user = super(UserFormCreation, self).save(commit=False)
    #     if self.userType == UserType.User:
    #         l_user.is_staff = False
    #         l_user.is_active = False
    #         l_user.is_superuser = False
    #     elif self.userType == UserType.Staff:
    #         l_user.company = ""
    #         l_user.is_staff = True
    #         l_user.is_active = False
    #         l_user.is_superuser = False
    #     elif self.userType == UserType.Admin:
    #         l_user.company = ""
    #         l_user.is_staff = True
    #         l_user.is_active = True
    #         l_user.is_superuser = True
    #     l_user.save()
    #     return l_user

class AdminUserForm(forms.ModelForm):
    '''
    This form will be use by Admin of website to create/update an account
    '''
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password', 'first_name', 'last_name', 'company', 'is_staff', 'is_active', 'is_superuser' ]
