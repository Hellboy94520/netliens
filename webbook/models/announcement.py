from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


from .user import User
import datetime

TITLE_MAX_LENGTH=50
NL_LEVEL_MAX=10
NL_LEVEL_MIN=0

class Statistics(models.Model):
    date_joined = models.DateTimeField(default=timezone.now())
    date_validation = models.DateTimeField(default=timezone.now())
    user_validation = models.ForeignKey(User,
                                        on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(default=timezone.now())


class Announcement(models.Model):
    title = models.CharField(max_length=TITLE_MAX_LENGTH,
                             default="",
                             blank=False,
                             null=False,
                             verbose_name=_("Title"),
                             help_text=_("Title of your announcement"))
    content = models.TextField(default="",
                               blank=False,
                               null=False,
                               verbose_name=_("Content"),
                               help_text=_("Content of your announcement"))
    image = models.ImageField(upload_to = "images/")
    website = models.URLField(default="",
                              verbose_name=_("Website"),
                              help_text=_("Your website address"))
    nllevel = models.IntegerField(validators=[MaxValueValidator(NL_LEVEL_MAX),
                                              MinValueValidator(NL_LEVEL_MIN)],
                                  default=0,
                                  verbose_name=_("NL Level"),
                                  help_text=_("NL Level of the website"))
    owner = models.ForeignKey(User, 
                              on_delete=models.CASCADE)
    is_enable = models.BooleanField(default=False,
                                    verbose_name=_("Enable"),
                                    help_text=_("Announcement is enabled"))
    is_valid = models.BooleanField(default=False,
                                   verbose_name=_("Valid"),
                                   help_text=_("Announcement is valid"))
    stats = models.OneToOneField(Statistics,
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Statistics"),
                                 help_text=_("Statistics of Announcement"))

    """ ---------------------------------------------------- """
    def get_statistics(self):
        return Statistics.objects.get(Announcement=self)
