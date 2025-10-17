import django.conf
import django.urls
from core.mixins import VoteableMixin
from core.rep_rules import REPUTATION_RULES
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from votes.models import Vote


class Question(VoteableMixin, models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solved = models.BooleanField(default=False)
    votes = GenericRelation(Vote)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return django.urls.reverse("forum:question_detail", kwargs={"pk": self.pk})

    def answers_count(self):
        return self.answers.count()


class Answer(VoteableMixin, models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    content = models.TextField()
    author = models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)
    votes = GenericRelation(Vote)

    class Meta:
        ordering = ["-is_accepted", "created_at"]

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.author.username}"

    def mark_accepted(self):
        if not self.is_accepted:
            self.is_accepted = True
            self.save()

            self.question.is_solved = True
            self.question.save()

            points = REPUTATION_RULES["answer_accepted"]
            self.author.profile.reputation_points += points
            self.author.profile.save()
