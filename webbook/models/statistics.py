from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .user import User

class Statistics(models.Model):
    date_creation = models.DateTimeField(default=timezone.now())
    user_creation = models.ForeignKey(
        User,
        related_name='user_creation',
        on_delete=models.RESTRICT)
    date_validation = models.DateTimeField(
        default = None,
        null=True,
        blank=True)
    user_validation = models.ForeignKey(
        User,
        default=None,
        related_name='user_validation',
        null=True,
        blank=True,
        on_delete=models.RESTRICT)
    last_update = models.DateTimeField(default=timezone.now())

