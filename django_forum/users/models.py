import django.conf
import django.contrib.auth.models
from django.db import models

import users.utils.validators


class User(django.contrib.auth.models.AbstractUser):
    class Role(models.TextChoices):
        GUEST = "G", "Guest"
        STUDENT = "S", "Student"
        ADMIN = "A", "Admin"

    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(choices=Role.choices, default=Role.GUEST, max_length=1)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"User {self.username}"

    def save(self, *args, **kwargs):
        is_new = self.id is None

        super().save(*args, **kwargs)

        if is_new:
            UserProfile.objects.get_or_create(user=self)


def avatar_upload_to(instance, filename: str) -> str:
    return f"users/{instance.user.username}/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        validators=[
            django.core.validators.FileExtensionValidator(["png", "jpg", "jpeg"]),
        ],
    )
    bio = models.TextField(blank=True)
    reputation_points = models.IntegerField(default=0, db_index=True)
    birthday = models.DateField(
        blank=True,
        null=True,
        validators=[
            users.utils.validators.YearRangeValidator(1925, -10),
        ],
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
