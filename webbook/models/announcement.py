from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models.signals import post_save

from .user import User
from .category import Category
from .language import LanguageModel
from .localisation import Localisation
from .statistics import Statistics

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', _("Only alphanumeric characters are allowed."))

TITLE_MAX_LENGTH=50
URL_MAX_LENGTH=100
NL_LEVEL_MAX=10


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Models
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Announcement(models.Model):
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
        default=None,
        blank=False,
        null=False,
        verbose_name=_("Category"),
        help_text=_("Announcement Category"))
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.DO_NOTHING,
        default=None,
        blank=False,
        null=False,
        verbose_name=_("Localisation"),
        help_text=_("Announcement Localisation"))
    # ReadOnly
    nl = models.PositiveIntegerField(
        validators=[MaxValueValidator(NL_LEVEL_MAX)],
        default=0,
        verbose_name=_("NL Level"),
        help_text=_("NL Level of the website"))
    # Private
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)
    is_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable"),
        help_text=_("Announcement is enabled"))
    is_valid = models.BooleanField(
        default=False,
        verbose_name=_("Valid"),
        help_text=_("Announcement is valid"))
    is_on_homepage = models.BooleanField(
        default=False,
        verbose_name=_("On Homepage"),
        help_text=_("Announcement is visible on Homepage"))

    """ ---------------------------------------------------- """
    def get_announcement_language(self, language: str):
        return AnnouncementLanguage.objects.get(
            announcement=self,
            language=language)

    """ ---------------------------------------------------- """
    def get_statistics(self):
        return AnnouncementStats.objects.get(announcement=self)

    class Meta:
        verbose_name = _("Announcement")


""" ---------------------------------------------------------------------------------------------------------------- """
class AnnouncementLanguage(LanguageModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_("Title"),
        help_text=_("Title of your announcement"))
    content = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("Content"),
        help_text=_("Content of your announcement"))
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE)


""" ---------------------------------------------------------------------------------------------------------------- """
class AnnouncementStats(Statistics):
    announcement = models.OneToOneField(Announcement, on_delete=models.CASCADE, primary_key=True)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def _annoucement_creation(instance, created, **kwargs):
    """
        Creation or update stat
    """
    if created:
        l_stat = AnnouncementStats(announcement=instance)
        l_stat.save()

post_save.connect(_annoucement_creation, sender = Announcement)
