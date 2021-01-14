from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Category, CategoryData, CategoryStats, get_all_category_in_order
from ..models import LanguageAvailable

""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
            Update order of parent ModelChoiceField
        """
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].choices = get_all_category_in_order()

    def is_valid(self):
        """
            Check if order unique for a same parent
        """
        if not super(CategoryForm, self).is_valid():
            return False

        if Category.objects.filter(
            parent=self.cleaned_data["parent"],
            order=self.cleaned_data["order"]
            ).exclude(pk=self.instance.id).count() > 0:
            self.add_error('order', _("A category with this order and parent already exist."))
            return False

        return True

    def save(self, *args, **kwargs):
        l_category = super(CategoryForm, self).save(commit=True)
        l_stat = CategoryStats(
            category=l_category,
            user_creation=kwargs['user'])
        # In case Category creation enabled the Category too
        if l_category.is_enable:
            l_stat.date_validation = l_stat.date_creation
            l_stat.user_validation = l_stat.user_creation
        l_stat.save()
        return l_category


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryDataForm(forms.ModelForm):
    language = forms.ChoiceField(
        choices=( (content.value, content.value) for content in LanguageAvailable),
        required=True,
        initial=None,
        label=_("Language"),
        help_text=_("Language of content"))

    class Meta:
        model = CategoryData
        fields = [ 'name', 'resume' ]

    def is_valid(self, category: Category):
        if not super(CategoryDataForm, self).is_valid():
            return False

        # Check if the language already exist for this category
        if CategoryData.objects.filter(
                language=self.cleaned_data['language'],
                category=category
            ).count() > 0:
            self.add_error('language', _("This language already exist for this category."))
            return False

        # Check if name is unique in all Category
        if CategoryData.objects.filter(
            name=self.cleaned_data['name'],
            language=self.cleaned_data['language']).count() > 0:
            self.add_error('name', _("A category with this name already exist."))
            return False

        self.category = category
        return True
        
    def save(self, *args, **kwargs):
        # Save 
        l_category = super(CategoryDataForm, self).save(commit=False)
        l_category.language = self.cleaned_data['language']
        l_category.category = self.category
        l_category.save()
        return l_category
