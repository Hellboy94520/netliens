from faulthandler import is_enabled
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_delete
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=1

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Models
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class NewCategory(models.Model):
    name = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_("Name"),
        help_text=_("This is the name shown to Users")
    )
    description = models.TextField(
        blank=True,
        null=False,
        verbose_name=_("Description"),
        help_text=_("This is a description of the name")
    )


# class Category(AdministrationModel, SqlImport):
#     parent = models.ForeignKey(
#         'Category',
#         default=None,
#         null=True,
#         blank=True,
#         verbose_name=_("Parent"),
#         help_text=_("Category parent"),
#         on_delete=models.DO_NOTHING)
#     # Indicated a personnalize order for category with same parents
#     order = models.PositiveIntegerField(
#         validators=[MinValueValidator(MINIMUM_ORDER)],
#         null=False,
#         blank=False,
#         default=MINIMUM_ORDER,
#         verbose_name=_("Order"),
#         help_text=_("Display order"))

#     """ ---------------------------------------------------- """
#     def get_categoryWithData(language: LanguageAvailable, order:str, **kwargs):
#         objectMap = {}
#         for category in Category.objects.filter(**kwargs).order_by(order):
#             objectMap[category] = category.get_data(language=language)
#         return objectMap

#     """ ---------------------------------------------------- """
#     def get_data(self, language: LanguageAvailable = LanguageAvailable.EN):
#         try:
#             return CategoryData.objects.get(category=self, language=language)
#         except ObjectDoesNotExist:
#             return None
#         except MultipleObjectsReturned:
#             #TODO: Send an email, case must not be possible
#             return None

#     """ ---------------------------------------------------- """
#     def get_childrenWithData_list(self, language: LanguageAvailable = LanguageAvailable.EN, **kwargs):
#         children = dict()
#         for child in Category.objects.filter(parent=self, **kwargs).order_by('order'):
#             childData = child.get_data(language)
#             children[child] = childData
#             children = children + child.get_childrenWithData_list(language=language, **kwargs)
#         return children


#     """ ---------------------------------------------------- """
#     def get_children_list(self, **kwargs):
#         children = list()
#         for child in Category.objects.filter(parent=self, **kwargs).order_by('order'):
#             children.append(child)
#             children.extend(child.get_children_list())
#         return children

#     class Meta:
#         verbose_name = _("Category")


""" ---------------------------------------------------------------------------------------------------------------- """
# class CategoryData(LanguageModel):
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE)



""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
# def _category_deletion(instance, **kwargs):
#     """
#         Deletion of Category need to change it children parent settings
#     """
#     for children in Category.objects.filter(parent=instance):
#         children.parent = instance.parent
#         children.save()

# pre_delete.connect(_category_deletion, sender = Category)

""" ------------------------------
Unknown Category
------------------------------ """
#TODO: For all Unknown model, add verification is_visible to False in main_consistency
# class UnknownCategory:
#     LANGUAGE_FR_NAME = "Inconnu"
#     LANGUAGE_FR_DESCRIPTION = \
#             "Categorie permettant de stocker les orphelins. Ne pas rendre visible !"
#     LANGUAGE_FR_LANGUAGE = LanguageAvailable.FR

#     LANGUAGE_EN_NAME = "Unknown"
#     LANGUAGE_EN_DESCRIPTION = \
#             "Category use to store lost. Do not set it visible !"
#     LANGUAGE_EN_LANGUAGE = LanguageAvailable.EN

#     PARENT = None
#     IS_ENABLE = True
#     IS_VISIBLE = False

# def createUnknownCategory(user):
#     category = Category.objects.create(
#         parent = UnknownCategory.PARENT,
#         is_enable = UnknownCategory.IS_ENABLE,
#         is_visible = UnknownCategory.IS_VISIBLE,
#         creation_user = user,
#         approval_date = datetime.now(),
#         approval_user = user
#     )
#     CategoryData.objects.create(
#         name = UnknownCategory.LANGUAGE_FR_NAME,
#         description = UnknownCategory.LANGUAGE_FR_DESCRIPTION,
#         language = UnknownCategory.LANGUAGE_FR_LANGUAGE,
#         category = category
#     )
#     CategoryData.objects.create(
#         name = UnknownCategory.LANGUAGE_EN_NAME,
#         description = UnknownCategory.LANGUAGE_EN_DESCRIPTION,
#         language = UnknownCategory.LANGUAGE_EN_LANGUAGE,
#         category = category
#     )

# def getUnknownCategory():
#     return CategoryData.objects.get(
#         name = UnknownCategory.LANGUAGE_EN_NAME,
#         description = UnknownCategory.LANGUAGE_EN_DESCRIPTION,
#         language = UnknownCategory.LANGUAGE_EN_LANGUAGE,
#         category__in=Category.objects.filter(
#             parent = UnknownCategory.PARENT,
#             is_enable = UnknownCategory.IS_ENABLE,
#             is_visible = UnknownCategory.IS_VISIBLE
#             )
#     ).category
