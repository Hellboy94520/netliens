from django.db import models
from django.utils.translation import ugettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices

TITLE_MAX_LENGTH=255

class Language(DjangoChoices):
    EN = ChoiceItem(1, "en")
    FR = ChoiceItem(2, "fr")

    def size():
        return 2

class LanguageModel(models.Model):
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
        default="",
        null=False,
        verbose_name=_("Description"),
        help_text=_("This is a description of the name")
    )
    language = models.IntegerField(
        default=Language.EN,
        choices=Language,
        verbose_name = _("Language"),
        help_text = _("Data language")
    )

    class Meta:
        abstract = True