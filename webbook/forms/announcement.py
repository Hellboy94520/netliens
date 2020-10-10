from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Announcement, AnnouncementStats
from ..models import Category, get_all_category_in_order
from ..models import Localisation, get_all_localisation_in_order

def _get_combinable_category():
    l_category_list = []
    for l_category in Category.objects.filter(parent=None).order_by('order'):
        l_category_list.append(l_category)
        l_category_list.extend(l_category.get_children_list())
    l_category_map = {}
    for l_category in l_category_list:
        if l_category.is_combinable:
            l_category_map[l_category.pk] = l_category
    return l_category_map

def _get_combinable_localisation():
    l_localisation_list = []
    for l_localisation in Category.objects.filter(parent=None).order_by('order'):
        l_localisation_list.append(l_localisation)
        l_localisation_list.extend(l_localisation.get_children_list())
    l_localisation_map = {}
    for l_localisation in l_localisation_list:
        if l_localisation.is_combinable:
            l_localisation_map[l_localisation.pk] = l_localisation
    return l_localisation_map

class AnnouncementUserForm(forms.ModelForm):
    nl = forms.ChoiceField(
        choices=[],
        required=True,
        initial=None,
        label=_("NL"),
        help_text=_("NL Level for your annoncement"))

    class Meta:
        model = Announcement
        fields = [ 'title', 'content', 'image', 'website', 'category', 'localisation' ]

    def __init__(self, user, *args, **kwargs):
        """
            Update nl function of User
        """
        super(AnnouncementUserForm, self).__init__(*args, **kwargs)
        # Owner
        self.owner = user
        # NL
        l_choices=[]
        if (user.nl0 - Announcement.objects.filter(owner=user, nl=0).count()) > 0:
            l_choices.extend([(0, '0')])
        if (user.nl1 - Announcement.objects.filter(owner=user, nl=1).count()) > 0:
            l_choices.extend([(1, '1')])
        if (user.nl2 - Announcement.objects.filter(owner=user, nl=2).count()) > 0:
            l_choices.extend([(2, '2')])
        if (user.nl3 - Announcement.objects.filter(owner=user, nl=3).count()) > 0:
            l_choices.extend([(3, '3')])
        if (user.nl4 - Announcement.objects.filter(owner=user, nl=4).count()) > 0:
            l_choices.extend([(4, '4')])
        if (user.nl5 - Announcement.objects.filter(owner=user, nl=5).count()) > 0:
            l_choices.extend([(5, '5')])
        if (user.nl6 - Announcement.objects.filter(owner=user, nl=6).count()) > 0:
            l_choices.extend([(6, '6')])
        if (user.nl7 - Announcement.objects.filter(owner=user, nl=7).count()) > 0:
            l_choices.extend([(7, '7')])
        self.fields['nl'].choices = l_choices
        # Category
        self.fields['category'].queryset = Category.objects.filter(pk__in=get_all_category_in_order(is_enable=True).keys())
        # Localisation
        self.fields['localisation'].queryset = Localisation.objects.filter(pk__in=get_all_localisation_in_order(is_enable=True).keys())

    def save(self, *args, **kwargs):
        l_announcement = super(AnnouncementUserForm, self).save(commit=False)
        l_announcement.owner = self.owner
        l_announcement.nl = self.cleaned_data['nl']
        l_announcement.is_enable = False
        l_announcement.is_valid = False
        l_announcement.save()