from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Localisation, LocalisationData, LocalisationStats, get_all_localisation_in_order
from ..models import LanguageAvailable

class LocalisationForm(forms.ModelForm):
    class Meta:
        model = Localisation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
            Update order of parent ModelChoiceField
        """
        super(LocalisationForm, self).__init__(*args, **kwargs)
        self.fields['parent'].choices = get_all_localisation_in_order()

    def is_valid(self):
        """
            Check if order unique for a same parent
        """
        if not super(LocalisationForm, self).is_valid():
            return False

        if Localisation.objects.filter(
            parent=self.cleaned_data["parent"],
            order=self.cleaned_data["order"]
            ).exclude(pk=self.instance.id).count() > 0:
            self.add_error('order', _("A localisation with this order and parent already exist."))
            return False

        return True

    def save(self, *args, **kwargs):
        l_localisation = super(LocalisationForm, self).save(commit=True)
        l_stat = LocalisationStats(
            localisation=l_localisation,
            user_creation=kwargs['user'])
        # In case Localisation creation enabled the Localisation too
        if l_localisation.is_enable:
            l_stat.date_validation = l_stat.date_creation
            l_stat.user_validation = l_stat.user_creation
        l_stat.save()
        return l_localisation


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationDataForm(forms.ModelForm):
    language = forms.ChoiceField(
        choices=( (content.value, content.value) for content in LanguageAvailable),
        required=True,
        initial=None,
        label=_("Language"),
        help_text=_("Language of content"))

    class Meta:
        model = LocalisationData
        fields = [ 'name', 'resume' ]

    def is_valid(self, localisation: Localisation):
        if not super(LocalisationDataForm, self).is_valid():
            return False

        # Check if the language already exist for this localisation
        if LocalisationData.objects.filter(
                language=self.cleaned_data['language'],
                localisation=localisation
            ).count() > 0:
            self.add_error('language', _("This language already exist for this localisation."))
            return False

        # Check if name is unique in all Localisation
        if LocalisationData.objects.filter(
            name=self.cleaned_data['name'],
            language=self.cleaned_data['language']).count() > 0:
            self.add_error('name', _("A localisation with this name already exist."))
            return False

        self.localisation = localisation
        return True
        
    def save(self, *args, **kwargs):
        # Save 
        l_localisation = super(LocalisationDataForm, self).save(commit=False)
        l_localisation.language = self.cleaned_data['language']
        l_localisation.localisation = self.localisation
        l_localisation.save()
        return l_localisation
