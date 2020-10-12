from django.db import models
from django.utils.translation import ugettext_lazy as _

TITLE_MAX_LENGTH = 128

class Homepage(models.Model):
    # Information Message
    information_title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default="Information Title",
        blank=True,
        null=True,
        verbose_name=_("Information Title"),
        help_text=_("Information Title show on Homepage if message not empty"))
    information_message = models.TextField(
        default="Information Message",
        blank=True,
        null=True,
        verbose_name=_("Information Message"),
        help_text=_("Information Message show on Homepage if not empty"))
    # Warning Message
    warning_title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default="Warning Title",
        blank=True,
        null=True,
        verbose_name=_("Warning Title"),
        help_text=_("Warning Title show on Homepage if message not empty"))
    warning_message = models.TextField(
        default="Warning Message",
        blank=True,
        null=True,
        verbose_name=_("Warning Message"),
        help_text=_("Warning Message show on Homepage if not empty"))
    # Important Message
    important_title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default="Important Title",
        blank=True,
        null=True,
        verbose_name=_("Important Title"),
        help_text=_("Important Title show on Homepage if message not empty"))
    important_message = models.TextField(
        default="Important Message",
        blank=True,
        null=True,
        verbose_name=_("Important Message"),
        help_text=_("Important Message show on Homepage if not empty"))

    # Unique instance model
    def save(self, *args, **kwargs):
        if not self.pk and Homepage.objects.exists():
            raise ValidationError('Only one instance can be created !')
        return super(Homepage, self).save(*args, **kwargs)
