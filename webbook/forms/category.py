from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [ 'name', 'resume', 'is_enable', 'parent', 'order' ]

    def __init__(self, *args, **kwargs):
        """
            Update order of parent ModelChoiceField
        """
        super(CategoryForm, self).__init__(*args, **kwargs)
        l_category_list = []
        for l_category in Category.objects.filter(parent=None).order_by('order'):
            l_category_list.append(l_category)
            l_category_list.extend(l_category.get_children_list())
        self.fields['parent'].choices = { l_category.pk : l_category for l_category in l_category_list }

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
