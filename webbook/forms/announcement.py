from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from ..models import LanguageAvailable
from ..models import Announcement, AnnouncementLanguage, AnnouncementStats, TITLE_MAX_LENGTH
from ..models import Category, get_all_category_in_order
from ..models import Localisation, get_all_localisation_in_order

class AnnouncementUserDataForm(forms.ModelForm):
    language = forms.ChoiceField(
        choices=( (content.value, content.value) for content in LanguageAvailable),
        required=True,
        initial=None,
        label=_("Language"),
        help_text=_("Language of content"))

    class Meta:
        model = AnnouncementLanguage
        fields = [ 'title', 'content' ]

    def is_valid(self, announcement: Announcement):
        if not super(AnnouncementUserDataForm, self).is_valid():
            return False
        # Check if the language exist or not for an announcement
        if AnnouncementLanguage.objects.filter(
                language=self.cleaned_data['language'],
                announcement=announcement
            ).count() > 0:
            self.add_error('language', _("This Language already exist for this announcement !"))
            return False

        self.announcement = announcement
        return True
        
    def save(self, *args, **kwargs):
        # Save 
        l_announcement = super(AnnouncementUserDataForm, self).save(commit=False)
        l_announcement.language = self.cleaned_data['language']
        l_announcement.announcement = self.announcement
        l_announcement.save()
        return l_announcement

class AnnouncementUserSettingForm(forms.ModelForm):
    nl = forms.ChoiceField(
        choices=[],
        required=True,
        initial=None,
        label=_("NL"),
        help_text=_("NL Level for your annoncement"))

    category = forms.ChoiceField(
        choices=[],
        required=True,
        initial=None,
        label=_("Category"),
        help_text=_("Choose a category for your announcement")
    )

    localisation = forms.ChoiceField(
        choices=[],
        required=True,
        initial=None,
        label=_("Localisation"),
        help_text=_("Choose a localisation for your announcement")
    )

    class Meta:
        model = Announcement
        fields = [ 'url', 'image', 'website' ]

    def __init__(self, *args, **kwargs):
        """
            Update nl function of User
        """
        # Owner
        self.owner = kwargs.pop('user', None)
        super(AnnouncementUserSettingForm, self).__init__(*args, **kwargs)
        # NL
        l_choices=[]
        if (self.owner.nl0 - Announcement.objects.filter(owner=self.owner, nl=0).count()) > 0:
            l_choices.extend([(0, '0')])
        if (self.owner.nl1 - Announcement.objects.filter(owner=self.owner, nl=1).count()) > 0:
            l_choices.extend([(1, '1')])
        if (self.owner.nl2 - Announcement.objects.filter(owner=self.owner, nl=2).count()) > 0:
            l_choices.extend([(2, '2')])
        if (self.owner.nl3 - Announcement.objects.filter(owner=self.owner, nl=3).count()) > 0:
            l_choices.extend([(3, '3')])
        if (self.owner.nl4 - Announcement.objects.filter(owner=self.owner, nl=4).count()) > 0:
            l_choices.extend([(4, '4')])
        if (self.owner.nl5 - Announcement.objects.filter(owner=self.owner, nl=5).count()) > 0:
            l_choices.extend([(5, '5')])
        if (self.owner.nl6 - Announcement.objects.filter(owner=self.owner, nl=6).count()) > 0:
            l_choices.extend([(6, '6')])
        if (self.owner.nl7 - Announcement.objects.filter(owner=self.owner, nl=7).count()) > 0:
            l_choices.extend([(7, '7')])
        self.fields['nl'].choices = l_choices
        # Category
        l_choices=[]
        for l_pk in get_all_category_in_order(is_enable=True):
            l_choices.extend([(l_pk, Category.objects.get(pk=l_pk))])
        self.fields['category'].choices = l_choices
        # Localisation
        l_choices=[]
        for l_pk in get_all_localisation_in_order(is_enable=True):
            l_choices.extend([(l_pk, Localisation.objects.get(pk=l_pk))])
        self.fields['localisation'].choices = l_choices

    def save(self, *args, **kwargs):
        l_announcement = super(AnnouncementUserSettingForm, self).save(commit=False)
        l_announcement.category = get_object_or_404(Category, pk=self.cleaned_data['category'])
        l_announcement.localisation = get_object_or_404(Localisation, pk=self.cleaned_data['localisation'])
        l_announcement.nl = self.cleaned_data['nl']
        l_announcement.owner = self.owner
        l_announcement.is_enable = False
        l_announcement.is_valid = False
        l_announcement.save()
        return l_announcement

class AnnouncementAdminForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'
