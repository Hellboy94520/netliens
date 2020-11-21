from django.db import models
from django.utils.translation import ugettext_lazy as _

from enum import Enum

class LanguageAvailable(Enum):
    EN = "EN"
    FR = "FR"    

class LanguageModel(models.Model):
    language = models.CharField(
        max_length=2,
        blank = False,
        null = False,
        verbose_name = _("Language"),
        help_text = _("Data language"))

    class Meta:
        abstract = True
