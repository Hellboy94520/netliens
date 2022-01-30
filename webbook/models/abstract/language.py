from django.db import models
from django.utils.translation import ugettext_lazy as _

TITLE_MAX_LENGTH=255

class LanguageAvailable:
    EN = "en"
    FR = "fr"

    def size():
        return 2

class Language(models.Model):
    """
        This is model that will manage languages in database
    """
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
    language = models.CharField(
        max_length=2,
        blank = False,
        null = False,
        verbose_name = _("Language"),
        help_text = _("Data language")
    )

    class Meta:
        abstract = True