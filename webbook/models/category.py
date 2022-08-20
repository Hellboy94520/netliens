import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_delete
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from webbook.models.abstract.administration import AdministrationModel
from webbook.models.abstract.language import LanguageModel, Language

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=1

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Models
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Category(AdministrationModel):
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
    parent = models.ForeignKey(
        'Category',
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Parent"),
        help_text=_("Category parent"),
        on_delete=models.DO_NOTHING
    )
    # Indicated a personnalize order for category with same parents
    order = models.PositiveIntegerField(
        validators=[MinValueValidator(MINIMUM_ORDER)],
        null=False,
        blank=False,
        default=MINIMUM_ORDER,
        verbose_name=_("Order"),
        help_text=_("Display order")
    )

    class Meta:
        verbose_name = _("Category")

    def __str__(self):
        return f"{self.pk}: {self.name}"
