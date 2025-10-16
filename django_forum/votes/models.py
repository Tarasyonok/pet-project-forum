from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Vote(models.Model):
    VOTE_TYPES = [
        ("up", "Upvote"),
        ("down", "Downvote"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "content_type", "object_id"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        vote_display = "upvoted" if self.vote_type == "up" else "downvoted"
        return f"{self.user.username} {vote_display} {self.content_object}"
