from django.urls import path

from leaderboards import views

app_name = "leaderboards"

urlpatterns = [
    path("", views.leaderboard_view, name="leaderboard"),
]
