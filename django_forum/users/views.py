import django.urls
from core.rep_rules import REPUTATION_RULES
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, FormView, UpdateView

from users.forms import ProfileEditForm, SignUpForm

User = get_user_model()


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = True
        new_user.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    def get_success_url(self):
        return django.urls.reverse("users:profile", kwargs={"username": self.request.user.username})


class PublicProfileView(DetailView):
    template_name = "users/public_profile.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context["questions_count"] = user.questions.count()
        context["answers_count"] = user.answers.count()
        context["reviews_count"] = user.reviews.count()
        context["accepted_answers"] = user.answers.filter(is_accepted=True).count()

        context["user_questions"] = (
            user.questions.select_related("author__profile").prefetch_related("answers").order_by("-created_at")[:10]
        )
        context["user_answers"] = user.answers.select_related(
            "question",
            "question__author",
            "author__profile",
        ).order_by("-created_at")[:10]
        context["user_reviews"] = user.reviews.select_related("author__profile").order_by("-created_at")[:10]

        question_upvotes = sum(question.get_upvotes().count() for question in user.questions.all())
        answer_upvotes = sum(answer.get_upvotes().count() for answer in user.answers.all())
        review_upvotes = sum(review.get_upvotes().count() for review in user.reviews.all())
        accepted_answers = user.answers.filter(is_accepted=True).count()

        context["question_upvotes"] = question_upvotes * REPUTATION_RULES["question_upvote"]
        context["answer_upvotes"] = answer_upvotes * REPUTATION_RULES["answer_upvote"]
        context["review_upvotes"] = review_upvotes * REPUTATION_RULES["review_upvote"]
        context["accepted_points"] = accepted_answers * REPUTATION_RULES["answer_accepted"]

        context["total_earned"] = (
            context["question_upvotes"]
            + context["answer_upvotes"]
            + context["review_upvotes"]
            + context["accepted_points"]
        )

        context["is_owner"] = self.request.user == user
        return context


class PrivateProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile_edit.html"
    form_class = ProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_instance"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def get_success_url(self):
        return django.urls.reverse("users:profile", kwargs={"username": self.request.user.username})
