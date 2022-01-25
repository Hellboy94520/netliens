from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_delete

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=1
MAX_CODE_LENGTH=5

from webbook.models.statistics import Statistics
from webbook.models.sqlimport import SqlImport
from webbook.models.language import LanguageModel, LanguageAvailable

def get_all_localisation_in_order(**kwargs):
    l_localisation_list = []
    for l_localisation in Localisation.objects.filter(parent=None, **kwargs).order_by('order'):
        l_localisation_list.append(l_localisation)
        l_localisation_list.extend(l_localisation.get_children_list(**kwargs))
    return { l_localisation.pk : l_localisation for l_localisation in l_localisation_list }


class Localisation(Statistics):
    # Code Iso3 if provided
    code    = models.CharField(
        max_length=MAX_CODE_LENGTH,
        verbose_name=_("Code"),
        blank=False,
        null=False,
        help_text=_("Localisation code"))
    # First column provide by Insee File
    insee = models.IntegerField(
        # unique=True, # TODO:Unique with the same parent !
        validators=[MinValueValidator(MINIMUM_ORDER)],
        default=MINIMUM_ORDER,
        verbose_name=_("Order"),
        help_text=_("Display order"))
    is_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable"),
        help_text=_("Localisation is enabled"))
    parent = models.ForeignKey(
        'Localisation',
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Parent"),
        help_text=_("Category parent"),
        on_delete=models.DO_NOTHING)
    # Indicated a personnalize order for Localisation with same parents
    order = models.PositiveIntegerField(
        validators=[MinValueValidator(MINIMUM_ORDER)],
        default=MINIMUM_ORDER,
        verbose_name=_("Order"),
        help_text=_("Display order"))
    # TODO: To delete after migration
    old_migrateStatus = models.TextField(default="")


    """ ---------------------------------------------------- """
    def get_localisationWithData(language: LanguageAvailable, order:str, **kwargs):
        objectMap = {}
        for localisation in Localisation.objects.filter(**kwargs).order_by(order):
            objectMap[localisation] = localisation.get_data(language=language)
        return objectMap

    """ ---------------------------------------------------- """
    def get_data(self, language: LanguageAvailable = LanguageAvailable.EN.value):
        return LocalisationData.objects.get(localisation=self, language=language)

    """ ---------------------------------------------------- """
    def get_children_list(self, **kwargs):
        children = list()
        for child in Localisation.objects.filter(parent=self, **kwargs).order_by('order'):
            children.append(child)
            children.extend(child.get_children_list())
        return children

    class Meta:
        verbose_name = _("Localisation")


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationData(LanguageModel):
    name = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_("Name"),
        help_text=_("Name of your localisation"))
    resume = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("Resume"),
        help_text=_("Resume of your localisation"))
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def _localisation_deletion(instance, **kwargs):
    """
        Deletion of Localisation need to change it children parent settings
    """
    for children in Localisation.objects.filter(parent=instance):
        children.parent = instance.parent
        children.save()

pre_delete.connect(_localisation_deletion, sender = Localisation)