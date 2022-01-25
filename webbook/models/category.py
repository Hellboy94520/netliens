from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_delete
from django.core.exceptions import ObjectDoesNotExist

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=1

from webbook.models.statistics import Statistics
from webbook.models.language import LanguageModel, LanguageAvailable
from webbook.models.sqlimport import SqlImport

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Models
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Category(Statistics, SqlImport):
    is_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable"),
        help_text=_("Category is enabled"))
    parent = models.ForeignKey(
        'Category',
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Parent"),
        help_text=_("Category parent"),
        on_delete=models.DO_NOTHING)
    # Indicated a personnalize order for category with same parents
    order = models.PositiveIntegerField(
        validators=[MinValueValidator(MINIMUM_ORDER)],
        null=False,
        blank=False,
        default=MINIMUM_ORDER,
        verbose_name=_("Order"),
        help_text=_("Display order"))

    """ ---------------------------------------------------- """
    def get_categoryWithData(language: LanguageAvailable, order:str, **kwargs):
        objectMap = {}
        for category in Category.objects.filter(**kwargs).order_by(order):
            objectMap[category] = category.get_data(language=language)
        return objectMap

    """ ---------------------------------------------------- """
    def get_data(self, language: LanguageAvailable = LanguageAvailable.EN.value):
        try:
            return CategoryData.objects.get(category=self, language=language)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            #TODO: Send an email, case must not be possible
            return None

    """ ---------------------------------------------------- """
    def get_childrenWithData_list(self, language: LanguageAvailable = LanguageAvailable.EN.value, **kwargs):
        children = dict()
        for child in Category.objects.filter(parent=self, **kwargs).order_by('order'):
            childData = child.get_data(language)
            children[child] = childData
            children = children + child.get_childrenWithData_list(language=language, **kwargs)
        return children


    """ ---------------------------------------------------- """
    def get_children_list(self, **kwargs):
        children = list()
        for child in Category.objects.filter(parent=self, **kwargs).order_by('order'):
            children.append(child)
            children.extend(child.get_children_list())
        return children

    class Meta:
        verbose_name = _("Category")


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryData(LanguageModel):
    name = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_("Name"),
        help_text=_("Name of the category"))
    resume = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("Resume"),
        help_text=_("Resume of the category"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE)



""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def _category_deletion(instance, **kwargs):
    """
        Deletion of Category need to change it children parent settings
    """
    for children in Category.objects.filter(parent=instance):
        children.parent = instance.parent
        children.save()

pre_delete.connect(_category_deletion, sender = Category)