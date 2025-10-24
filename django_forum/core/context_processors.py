from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from forum.models import Answer, Question
from reviews.models import CourseReview
from users.models import UserProfile
from votes.models import Vote


def community_stats(request):
    context = {}

    context["total_questions"] = Question.objects.count()
    context["total_answers"] = Answer.objects.count()
    context["total_reviews"] = CourseReview.objects.count()

    context["solved_questions"] = Question.objects.filter(is_solved=True).count()
    context["active_questions"] = Question.objects.filter(is_solved=False).count()

    if CourseReview.objects.exists():
        context["avg_rating"] = round(CourseReview.objects.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0, 1)

        review_content_type = ContentType.objects.get_for_model(CourseReview)
        context["total_helpful_votes"] = Vote.objects.filter(content_type=review_content_type, vote_type="up").count()
    else:
        context["avg_rating"] = 0
        context["total_helpful_votes"] = 0

    context["total_courses"] = CourseReview.objects.values("course_name").distinct().count()

    context["total_votes"] = Vote.objects.count()

    context["accepted_answers"] = Answer.objects.filter(is_accepted=True).count()

    top_profile = UserProfile.objects.order_by("-reputation_points").first()
    if top_profile:
        context["top_user"] = top_profile.user.username
        context["top_reputation"] = top_profile.reputation_points

        context["top_user_questions"] = top_profile.user.questions.count()
        context["top_user_answers"] = top_profile.user.answers.count()
        context["top_user_reviews"] = top_profile.user.reviews.count()
    else:
        context["top_user"] = "No users yet"
        context["top_reputation"] = 0
        context["top_user_questions"] = 0
        context["top_user_answers"] = 0
        context["top_user_reviews"] = 0

    return context
