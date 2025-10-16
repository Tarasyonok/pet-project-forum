from django.urls import path

from votes import views

app_name = "votes"

urlpatterns = [
    path("<int:content_type_id>/<int:object_id>/<str:vote_type>/", views.vote, name="vote"),
]
