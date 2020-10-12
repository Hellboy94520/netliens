from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Homepage

class HomepageForm(forms.ModelForm):
    class Meta:
        model = Homepage
        fields = '__all__'
