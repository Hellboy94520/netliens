from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from ..models import ActivationEmail

import logging
logger = logging.getLogger("forms")


class ActivationEmailForm(forms.ModelForm):
    '''
    This form will be use to update ActivationEmail message
    '''
    class Meta:
        model = ActivationEmail
        fields = [ 'subject', 'message' ]
