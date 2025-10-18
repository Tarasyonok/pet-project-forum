from forum.models import Answer, Question
from reviews.models import CourseReview
from users.models import UserProfile


def community_stats(request):
    context = {}

    context["total_questions"] = Question.objects.count()
    context["total_answers"] = Answer.objects.count()
    context["total_reviews"] = CourseReview.objects.count()

    top_profile = UserProfile.objects.order_by("-reputation_points").first()
    if top_profile:
        context["top_user"] = top_profile.user.username
        context["top_reputation"] = top_profile.reputation_points
    else:
        context["top_user"] = "No users yet"
        context["top_reputation"] = 0

    return context
