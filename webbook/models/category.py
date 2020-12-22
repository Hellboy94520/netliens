from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_delete

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=1

from .statistics import Statistics
from .language import LanguageModel

def get_all_category_in_order(**kwargs):
    l_category_list = []
    for l_category in Category.objects.filter(parent=None, **kwargs).order_by('order'):
        l_category_list.append(l_category)
        l_category_list.extend(l_category.get_children_list(**kwargs))
    return { l_category.pk : l_category for l_category in l_category_list }


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Models
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Category(models.Model):
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
    def get_statistics(self):
        return CategoryStatistics.objects.get(category=self)

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
        verbose_name=_("Title"),
        help_text=_("Title of your category"))
    resume = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("Content"),
        help_text=_("Content of your category"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE)


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryStats(Statistics):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def _category_creation(instance, created, **kwargs):
    """
        Creation or update stat
    """
    if created:
        l_stat = CategoryStats(category=instance)
        l_stat.save()

post_save.connect(_category_creation, sender = Category)

def _category_deletion(instance, **kwargs):
    """
        Deletion of Category need to change it children parent settings
    """
    for children in Category.objects.filter(parent=instance):
        children.parent = instance.parent
        children.save()

pre_delete.connect(_category_deletion, sender = Category)