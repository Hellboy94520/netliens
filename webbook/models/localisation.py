from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_delete

from datetime import datetime

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=0
MINIMUM_INSEE=0
MAX_CODE_LENGTH=5

from webbook.models.abstract.model_administration import ModelAdministration
from webbook.models.abstract.statistics import Statistics
from webbook.models.abstract.language import Language as LanguageModel
from webbook.models.abstract.language import LanguageAvailable

def get_all_localisation_in_order(**kwargs):
    l_localisation_list = []
    for l_localisation in Localisation.objects.filter(parent=None, **kwargs).order_by('order'):
        l_localisation_list.append(l_localisation)
        l_localisation_list.extend(l_localisation.get_children_list(**kwargs))
    return { l_localisation.pk : l_localisation for l_localisation in l_localisation_list }


class Localisation(ModelAdministration, Statistics):
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
        validators=[MinValueValidator(MINIMUM_INSEE)],
        default=MINIMUM_INSEE,
        verbose_name=_("Order"),
        help_text=_("Display order"))
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
    #TODO: TMP: To delete after migrations
    old_migrateStatus = models.TextField(
        default=""
    )


    """ ---------------------------------------------------- """
    def get_localisationWithData(language: LanguageAvailable, order:str, **kwargs):
        objectMap = {}
        for localisation in Localisation.objects.filter(**kwargs).order_by(order):
            objectMap[localisation] = localisation.get_data(language=language)
        return objectMap

    """ ---------------------------------------------------- """
    def get_data(self, language: LanguageAvailable = LanguageAvailable.EN):
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

""" ------------------------------
Unknown Localisation
------------------------------ """
#TODO: For all Unknown model, add verification is_visible to False in main_consistency
class UnknownLocalisation:
    LANGUAGE_FR_NAME = "Inconnu"
    LANGUAGE_FR_DESCRIPTION = \
            "Localisation permettant de stocker les orphelins. Ne pas rendre visible !"
    LANGUAGE_FR_LANGUAGE = LanguageAvailable.FR

    LANGUAGE_EN_NAME = "Unknown"
    LANGUAGE_EN_DESCRIPTION = \
            "Localisation use to store lost. Do not set it visible !"
    LANGUAGE_EN_LANGUAGE = LanguageAvailable.EN

    CODE = "NONE"
    INSEE = 0
    ORDER = 0
    PARENT = None
    IS_ENABLE = True
    IS_VISIBLE = False

    def getFieldsDataFr():
        return {
            "name": UnknownLocalisation.LANGUAGE_FR_NAME,
            "description": UnknownLocalisation.LANGUAGE_FR_DESCRIPTION,
            "language": UnknownLocalisation.LANGUAGE_FR_LANGUAGE
        }
    def getFieldsDataEn():
        return {
            "name": UnknownLocalisation.LANGUAGE_EN_NAME,
            "description": UnknownLocalisation.LANGUAGE_EN_DESCRIPTION,
            "language": UnknownLocalisation.LANGUAGE_EN_LANGUAGE
        }
    def getFields():
        toto = UnknownLocalisation.INSEE
        return {
            "code": UnknownLocalisation.CODE,
            "insee": UnknownLocalisation.INSEE,
            "order": UnknownLocalisation.ORDER,
            "parent": UnknownLocalisation.PARENT,
            "is_enable": UnknownLocalisation.IS_ENABLE,
            "is_visible": UnknownLocalisation.IS_VISIBLE
        }


def createUnknownLocalisation(user):
    localisation = Localisation.objects.create(
        code = UnknownLocalisation.CODE,
        insee = UnknownLocalisation.INSEE,
        order = UnknownLocalisation.ORDER,
        # parent = UnknownLocalisation.PARENT,
        is_enable = UnknownLocalisation.IS_ENABLE,
        is_visible = UnknownLocalisation.IS_VISIBLE,
        creation_user = user,
        approval_date = datetime.now(),
        approval_user = user
    )
    LocalisationData.objects.create(
        name = UnknownLocalisation.LANGUAGE_FR_NAME,
        description = UnknownLocalisation.LANGUAGE_FR_DESCRIPTION,
        language = UnknownLocalisation.LANGUAGE_FR_LANGUAGE,
        category = localisation
    )
    LocalisationData.objects.create(
        name = UnknownLocalisation.LANGUAGE_EN_NAME,
        description = UnknownLocalisation.LANGUAGE_EN_DESCRIPTION,
        language = UnknownLocalisation.LANGUAGE_EN_LANGUAGE,
        category = localisation
    )

def getUnknownLocalisation():
    return LocalisationData.objects.get(
        name = UnknownLocalisation.LANGUAGE_EN_NAME,
        description = UnknownLocalisation.LANGUAGE_EN_DESCRIPTION,
        language = UnknownLocalisation.LANGUAGE_EN_LANGUAGE,
        localisation__in=Localisation.objects.filter(
            code = UnknownLocalisation.CODE,
            insee = UnknownLocalisation.INSEE,
            order = UnknownLocalisation.ORDER,
            parent = UnknownLocalisation.PARENT,
            is_enable = UnknownLocalisation.IS_ENABLE,
            is_visible = UnknownLocalisation.IS_VISIBLE
            )
    ).localisation
