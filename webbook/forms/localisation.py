from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Localisation, get_all_localisation_in_order

class LocalisationForm(forms.ModelForm):
    class Meta:
        model = Localisation
        fields = [ 'name', 'resume', 'code', 'is_enable', 'parent', 'order' ]

    def __init__(self, *args, **kwargs):
        """
            Update order of parent ModelChoiceField
        """
        super(LocalisationForm, self).__init__(*args, **kwargs)
        self.fields['parent'].choices = get_all_localisation_in_order()

    def clean(self):
        """
            Check if order and name are unique for a same parent
        """
        cleaned_data = super(LocalisationForm, self).clean()
        if Localisation.objects.filter(parent=cleaned_data.get("parent"), name=cleaned_data.get("name")).exclude(pk=self.instance.id).count() > 0:
            self.add_error('name', _("A localisation with this name and parent already exist."))
        if Localisation.objects.filter(parent=cleaned_data.get("parent"), order=cleaned_data.get("order")).exclude(pk=self.instance.id).count() > 0:
            self.add_error('order', _("A localisation with this order and parent already exist."))
        return cleaned_data
