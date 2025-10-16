from django.urls import path

from forum import views

app_name = "forum"

urlpatterns = [
    # Questions
    path("", views.QuestionListView.as_view(), name="question_list"),
    path("question/<int:pk>/", views.QuestionDetailView.as_view(), name="question_detail"),
    path("question/new/", views.QuestionCreateView.as_view(), name="question_create"),
    path("question/<int:pk>/edit/", views.QuestionUpdateView.as_view(), name="question_update"),
    path("question/<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="question_delete"),
    # Answers
    path("question/<int:question_id>/answer/", views.AnswerCreateView.as_view(), name="answer_create"),
    path("answer/<int:pk>/edit/", views.AnswerUpdateView.as_view(), name="answer_update"),
    path("answer/<int:pk>/delete/", views.AnswerDeleteView.as_view(), name="answer_delete"),
    path("answer/<int:pk>/accept/", views.accept_answer, name="answer_accept"),
]
