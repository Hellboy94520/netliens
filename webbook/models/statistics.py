from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .user import User

class Statistics(models.Model):
    date_joined = models.DateTimeField(default=timezone.now())
    date_validation = models.DateTimeField(default=timezone.now())
    user_validation = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(default=timezone.now())

