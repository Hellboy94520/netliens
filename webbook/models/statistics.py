from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from webbook.models.user import User

class Statistics(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    creation_user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="%(class)s_creation_user"
    )
    last_update_date = models.DateTimeField(auto_now=True)
    approval_date = models.DateTimeField(
        default = None,
        null=True,
        blank=True
    )
    approval_user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="%(class)s_approval_user"
    )
    class Meta:
        abstract = True