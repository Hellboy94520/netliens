from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from ..models import User, UserType

import logging
logger = logging.getLogger("forms")

class UserFormCreation(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password', 'first_name', 'last_name', 'company' ]

    def __init__(self, userType: UserType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if userType == UserType.User:
            self.fields['company'].required = True
        elif userType == UserType.Staff:
            self.fields['company'].required = False
        elif userType == UserType.Admin:
            self.fields['company'].required = False
        else:
            raise ValidationError("userType input argument incorrect !")
        self.userType = userType

    # def clean(self):
    #    email = self.cleaned_data.get('email')
    #    if not email:
    #        self.add_error('email', _("This field is required."))
    #    if User.objects.filter(email=email).exists():
    #        self.add_error('email', _("Email already exists !"))
    #    return self.cleaned_data

    def save(self, *args, **kwargs):
        l_user = super(UserFormCreation, self).save(commit=False)
        if self.userType == UserType.User:
            l_user.is_staff = False
            l_user.is_active = False
            l_user.is_superuser = False
        elif self.userType == UserType.Staff:
            l_user.company = ""
            l_user.is_staff = True
            l_user.is_active = False
            l_user.is_superuser = False
        elif self.userType == UserType.Admin:
            l_user.company = ""
            l_user.is_staff = True
            l_user.is_active = True
            l_user.is_superuser = True
        else:
            raise ValidationError("userType input argument incorrect !")
        l_user.save()
        return l_user
