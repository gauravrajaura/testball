# Std imports
import uuid as uuid

# Django imports
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

# Third party imports
from model_utils.models import TimeStampedModel

# Local imports



validator_mobile_number = RegexValidator(
    regex=r"^[1-9]\d{9}$", message="Invalid Mobile Number"
)


class StatusMixinManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(StatusMixinManager, self).filter(is_deleted=False)

    def filter(self, *args, **kwargs):
        return (
            super(StatusMixinManager, self)
            .filter(is_active=True, is_deleted=False)
            .filter(*args, **kwargs)
        )

    def active(self, *args, **kwargs):
        return super(StatusMixinManager, self).filter(is_active=True, is_deleted=False)
    
class StatusMixin(models.Model):
    is_active = models.BooleanField(_("active"), default=True, blank=False, null=False)
    is_deleted = models.BooleanField(
        _("deleted"), default=False, blank=False, null=False
    )
    objects = StatusMixinManager

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        if self.is_active:
            self.is_deleted = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.CharField(
        max_length=60, help_text="Maximum 50 characters", db_index=True, unique=True
    )

    class Meta:
        abstract = True


class UUIDMixin(TimeStampedModel, StatusMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class IPAddressMixin(models.Model):
    ip_address = models.GenericIPAddressField(_('IP Address'), blank=True, null=True)

    class Meta:
        abstract = True
