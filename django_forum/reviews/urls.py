from django.urls import path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="review_list"),
    path("review/<int:pk>/", views.ReviewDetailView.as_view(), name="review_detail"),
    path("review/new/", views.ReviewCreateView.as_view(), name="review_create"),
    path("review/<int:pk>/edit/", views.ReviewUpdateView.as_view(), name="review_update"),
    path("review/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review_delete"),
    path("user/<str:username>/", views.UserReviewListView.as_view(), name="user_reviews"),
]
