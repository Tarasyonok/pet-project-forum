import django.conf
import django.urls
import django.utils.timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.mixins import VoteableMixin
from votes.models import Vote


class CourseReview(VoteableMixin, models.Model):
    RATING_CHOICES = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]

    author = models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    course_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(Vote)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["author", "course_name"]

    def __str__(self):
        return f"{self.course_name} - {self.get_rating_stars()} by {self.author.username}"

    def get_absolute_url(self):
        return django.urls.reverse("reviews:review_detail", kwargs={"pk": self.pk})

    def get_rating_stars(self):
        return "⭐" * self.rating
