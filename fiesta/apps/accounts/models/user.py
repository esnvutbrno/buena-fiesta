from __future__ import annotations

import typing

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import ModificationDateTimeField

if typing.TYPE_CHECKING:
    from apps.accounts.models import UserProfile


class User(AbstractUser):
    class State(models.TextChoices):
        REGISTERED = "registered", _("Registered")
        ACTIVE = "active", _("Active")
        EXPIRED = "expired", _("Expired")
        BANNED = "banned", _("Banned")

    state = models.CharField(
        choices=State.choices,
        default=State.REGISTERED,
        max_length=16,
        verbose_name=_("state"),
        help_text=_("current state of user (different from user profile state)"),
    )

    modified = ModificationDateTimeField(verbose_name=_("modified"))

    @property
    def profile_or_none(self) -> typing.Optional["UserProfile"]:
        from apps.accounts.models import UserProfile

        try:
            return self.profile
        except UserProfile.DoesNotExist:
            ...

    class Meta(AbstractUser.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("users")


__all__ = ["User"]
