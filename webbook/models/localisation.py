from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save

TITLE_MAX_LENGTH=50
MINIMUM_ORDER=1
MAX_CODE_LENGTH=5

from .statistics import Statistics

class Localisation(models.Model):
    name = models.CharField(max_length=TITLE_MAX_LENGTH,
                            default="",
                            blank=False,
                            null=False,
                            verbose_name=_("Name"),
                            help_text=_("Name of the category"))
    resume = models.TextField(default="",
                              blank=True,
                              null=True,
                              verbose_name=_("Resume"),
                              help_text=_("Resume of the category"))
    code    = models.CharField(max_length=MAX_CODE_LENGTH,
                               verbose_name="Code",
                               blank=False,
                               null=False,
                               help_text=_("Localisation code"))
    is_enable = models.BooleanField(default=False,
                                    verbose_name=_("Enable"),
                                    help_text=_("Category is enabled"))
    parent    = models.ForeignKey('Localisation',
                                  default=None,
                                  null=True,
                                  blank=True,
                                  verbose_name=_("Parent"),
                                  help_text=_("Category parent"),
                                  on_delete=models.DO_NOTHING)
    # Indicated a personnalize order for Localisation with same parents
    order = models.PositiveIntegerField(validators=[MinValueValidator(MINIMUM_ORDER)],
                                        default=MINIMUM_ORDER,
                                        verbose_name=_("Order"),
                                        help_text=_("Display order"))

    """ ---------------------------------------------------- """
    def get_statistics(self):
        return LocalisationStats.objects.get(localisation=self)

    """ ---------------------------------------------------- """
    def get_children_list(self):
        children = list()
        for child in Localisation.objects.filter(parent=self).order_by('order'):
            children.append(child)
            children.extend(child.get_children_list())
        return children

    class Meta:
        verbose_name = _("Localisation")


class LocalisationStats(Statistics):
    localisation = models.OneToOneField(Localisation, on_delete=models.CASCADE, primary_key=True)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Signals
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def _localisation_creation(instance, created, **kwargs):
    """
        Creation or update stat
    """
    if created:
        l_stat = LocalisationStats(localisation=instance)
        l_stat.save()

post_save.connect(_localisation_creation, sender = Localisation)
