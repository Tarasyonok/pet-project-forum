from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from users.models import UserProfile, User


def leaderboard_view(request):
    all_time_leaders = (
        UserProfile.objects.select_related("user")
        .filter(reputation_points__gt=0)
        .order_by("-reputation_points")[:20]
    )

    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    this_month_active = User.objects.filter(
        Q(questions__created_at__gte=month_start)
        | Q(answers__created_at__gte=month_start)
        | Q(reviews__created_at__gte=month_start),
    ).distinct()

    month_leaders = UserProfile.objects.filter(user__in=this_month_active).order_by("-reputation_points")[:10]

    context = {
        "all_time_leaders": all_time_leaders,
        "month_leaders": month_leaders,
    }

    return render(request, "leaderboards/leaderboard.html", context)