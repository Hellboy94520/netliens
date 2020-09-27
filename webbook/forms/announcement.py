from django import forms

from ..models import Announcement, AnnouncementStats

class AnnouncementUserForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [ 'title', 'content', 'image', 'website', 'nllevel' ]
    #TODO: Add to 'website' info to add https for website in http because Django add automatically http in case it does not exist
    #TODO: Level has to be select from a list which is fill with what the user choose

class AnnouncementAdminForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [ 'title', 'content', 'image', 'website', 'nllevel', 'owner', 'is_enable', 'is_valid' ]
