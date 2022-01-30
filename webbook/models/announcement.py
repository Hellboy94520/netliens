from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models.signals import pre_delete

from webbook.models.user import User
from webbook.models.category import Category
from webbook.models.abstract.language import Language as LanguageModel
from webbook.models.localisation import Localisation
from webbook.models.abstract.administration import Administration as AdministrationModel
from webbook.models.abstract.sqlimport import SqlImport

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', _("Only alphanumeric characters are allowed."))

TITLE_MAX_LENGTH=50
URL_MAX_LENGTH=100
NL_LEVEL_MAX=10


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Models
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Announcement(AdministrationModel, SqlImport):
    # Updatable by User
    url = models.CharField(
        default="",
        unique=True,
        blank=False,
        null=False,
        max_length=URL_MAX_LENGTH,
        verbose_name=_("Url"),
        help_text=_("Choose an url as following for the referencing: www.net-liens.com/announcement/<url>"),
        validators=[alphanumeric])
    image = models.ImageField(upload_to = "images/",
        default=None,
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_("Image of your announcement"))
    website = models.URLField(
        default="",
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Website"),
        help_text=_("Your website address"))
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Category"),
        help_text=_("Announcement Category"))
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Localisation"),
        help_text=_("Announcement Localisation"))
    return_url = models.CharField(
        default="",
        blank=True,
        null=True,
        max_length=URL_MAX_LENGTH,
        verbose_name=_("Return Url"),
        help_text=_("Return Url used to link that announcement"))
    # ReadOnly by User
    nl = models.PositiveIntegerField(
        validators=[MaxValueValidator(NL_LEVEL_MAX)],
        default=0,
        verbose_name=_("NL Level"),
        help_text=_("NL Level of the website"))
    click_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Click"),
        help_text=_("Announcement click quantity"))
    return_url_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Return"),
        help_text=_("Return Url quantity"))
    # Private
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    is_visible_by_officetourisme = models.BooleanField(
        default=False,
        verbose_name=_("Visibility on Office Tourisme"),
        help_text=_("Set is this announcement is visible by Office Tourisme website")
    )

    """ ---------------------------------------------------- """
    def get_announcement_language(self, language: str):
        return AnnouncementData.objects.get(
            announcement=self,
            language=language)

    class Meta:
        verbose_name = _("Announcement")


""" ---------------------------------------------------------------------------------------------------------------- """
class AnnouncementData(LanguageModel):
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
# def _category_deletion(instance, **kwargs):
#     """
#         Deletion of a category
#     """
#     for announcement in Announcement.objects.filter(category=instance):
#         announcement.category = instance.parent
#         announcement.save()

# pre_delete.connect(_category_deletion, sender = Category)