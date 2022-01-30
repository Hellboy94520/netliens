from django.db import models

class SqlImport(models.Model):
    """
        This is a temporary model to save data from Sql Import
    """
    old_sqlId = models.IntegerField(
        default=-1,
        unique=True,
        blank=False,
        null=False
    )
    old_migrateStatus = models.TextField(
        default=""
    )

    class Meta:
        abstract = True