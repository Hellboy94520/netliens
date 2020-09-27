from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ 'name', 'resume', 'is_enable', 'parent', 'order' ]

    # TODO:
    def __init__(self, *args, **kwargs):
        """
            Change the order of parent ModelChoiceField
        """
        super(CategoryForm, self).__init__(*args, **kwargs)
        # Get required values
        # for l_category_list in Category.objects.filter(parent=None).order_by('order'):
        #     l_list.append(l_localisation)
        # # Creation of new choices tab (with default value)
        # l_choices = []
        # l_choices.append(('', dict(self.fields['parent'].choices)['']))
        # for l_localisation in l_list:
        #     l_string = string.whitespace*l_localisation.level*2
        #     l_choices.append((l_localisation.pk, f"{l_string} {l_localisation}"))
        # self.fields['parent'].choices = l_choices


    def clean(self):
        """
            Check if order and name are unique for a same parent
        """
        cleaned_data = super(CategoryForm, self).clean()
        if Category.objects.filter(parent=cleaned_data.get("parent"), name=cleaned_data.get("name")).exclude(pk=self.instance.id).count() > 0:
            self.add_error('name', _("A category with this name and parent already exist."))
        if Category.objects.filter(parent=cleaned_data.get("parent"), order=cleaned_data.get("order")).exclude(pk=self.instance.id).count() > 0:
            self.add_error('order', _("A category with this order and parent already exist."))
        return cleaned_data
