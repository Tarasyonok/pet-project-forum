from datetime import timedelta

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from forum.models import Answer, Question
from reviews.models import CourseReview
from users.models import UserProfile

User = get_user_model()


def home_view(request):
    context = {}

    context["total_users"] = User.objects.count()
    context["total_questions"] = Question.objects.count()
    context["total_answers"] = Answer.objects.count()
    context["total_reviews"] = CourseReview.objects.count()

    context["latest_questions"] = (
        Question.objects.select_related("author", "author__profile")
        .prefetch_related("answers")
        .order_by("-created_at")[:8]
    )

    context["latest_reviews"] = CourseReview.objects.select_related("author", "author__profile").order_by(
        "-created_at",
    )[:6]

    context["top_contributors"] = (
        UserProfile.objects.select_related("user").filter(reputation_points__gt=0).order_by("-reputation_points")[:5]
    )

    day_ago = timezone.now() - timedelta(hours=24)
    context["questions_tonight"] = Question.objects.filter(created_at__gte=day_ago).count()
    context["total_answers_tonight"] = Answer.objects.filter(created_at__gte=day_ago).count()

    top_profile = UserProfile.objects.order_by("-reputation_points").first()
    if top_profile:
        context["top_user"] = top_profile.user.username
        context["top_reputation"] = top_profile.reputation_points

    if request.user.is_authenticated:
        user = request.user
        context["user_questions"] = user.questions.count()
        context["user_answers"] = user.answers.count()
        context["user_reviews"] = user.reviews.count()

        user_rank = UserProfile.objects.filter(reputation_points__gt=user.profile.reputation_points).count() + 1
        context["user_rank"] = user_rank

    return render(request, "home/home.html", context)


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


def panda(request):
    raise Http404("Page not found")
