from django.contrib.contenttypes.models import ContentType
from votes.models import Vote

from core.rep_rules import REPUTATION_RULES


class VoteableMixin:
    def get_votes(self):
        content_type = ContentType.objects.get_for_model(self)
        return Vote.objects.filter(content_type=content_type, object_id=self.pk)

    def get_upvotes(self):
        return self.get_votes().filter(vote_type="up")

    def get_downvotes(self):
        return self.get_votes().filter(vote_type="down")

    def get_vote_count(self):
        return self.get_upvotes().count() - self.get_downvotes().count()

    def get_user_vote(self, user):
        if user is None or not user.is_authenticated:
            return None

        content_type = ContentType.objects.get_for_model(self)
        try:
            vote = Vote.objects.get(user=user, content_type=content_type, object_id=self.pk)
            return vote.vote_type
        except Vote.DoesNotExist:
            return None

    def vote(self, user, vote_type):
        if user is None or not user.is_authenticated:
            return False

        if hasattr(self, "author") and self.author == user:
            return False

        content_type = ContentType.objects.get_for_model(self)

        try:
            vote = Vote.objects.get(user=user, content_type=content_type, object_id=self.pk)

            if vote.vote_type == vote_type:
                old_vote_type = vote.vote_type
                vote.delete()
                if hasattr(self, "author") and self.author != user:
                    self._update_reputation(old_vote_type, removed=True)
                return "removed"
            else:
                old_vote_type = vote.vote_type
                vote.vote_type = vote_type
                vote.save()
                if hasattr(self, "author") and self.author != user:
                    self._update_reputation(old_vote_type, new_vote_type=vote_type)
                return "updated"

        except Vote.DoesNotExist:
            Vote.objects.create(user=user, content_type=content_type, object_id=self.pk, vote_type=vote_type)
            if hasattr(self, "author") and self.author != user:
                self._update_reputation(vote_type)
            return "added"

    def _update_reputation(self, vote_type, *, removed=False, new_vote_type=None):
        model_name = self.__class__.__name__.lower()

        if model_name == "coursereview":
            model_name = "review"

        vote_suffix = "upvote" if vote_type == "up" else "downvote"
        reputation_key = f"{model_name}_{vote_suffix}"

        if removed:
            points = -REPUTATION_RULES.get(reputation_key, 0)
        elif new_vote_type:
            old_suffix = "upvote" if vote_type == "up" else "downvote"
            new_suffix = "upvote" if new_vote_type == "up" else "downvote"
            old_points = REPUTATION_RULES.get(f"{model_name}_{old_suffix}", 0)
            new_points = REPUTATION_RULES.get(f"{model_name}_{new_suffix}", 0)
            points = new_points - old_points
        else:
            # New vote
            points = REPUTATION_RULES.get(reputation_key, 0)

        # Update reputation
        self.author.profile.reputation_points += points
        self.author.profile.save()
