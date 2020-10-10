from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class Email(models.Model):
    subject = models.TextField(
        default="",
        blank=False,
        null=False,
        verbose_name=_("Subject"),
        help_text=_("Subject of the email"))
    message = models.TextField(
        default="",
        blank=False,
        null=False,
        verbose_name=_("Message"),
        help_text=_("Message of the email"))

    class Meta:
        verbose_name = _("Email")

class ActivationEmail(Email):
    pass

    def save(self, *args, **kwargs):
        if not self.pk and ActivationEmail.objects.exists():
            raise ValidationError('Only one ActivationEmail instance can be created !')
        return super(ActivationEmail, self).save(*args, **kwargs)

ActivationEmail._meta.get_field('subject').default = "Activation Email Link"
ActivationEmail._meta.get_field('message').default = "This is an activation Email"
