import django.urls
from django import forms
from django.utils.translation import gettext_lazy as _

from reviews.models import CourseReview


class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ["course_name", "title", "content", "rating"]
        widgets = {
            "course_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("e.g., Django Masterclass, Python Basics...")},
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Brief summary of your review...")},
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Share your experience with this course..."),
                    "rows": 5,
                },
            ),
            "rating": forms.RadioSelect(choices=CourseReview.RATING_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs.update({"class": "form-check-inline"})

    def clean(self):
        cleaned_data = super().clean()
        course_name = cleaned_data.get("course_name")

        if self.user and course_name:
            existing_review = CourseReview.objects.filter(
                author=self.user,
                course_name=course_name,
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing_review.exists():
                raise forms.ValidationError(
                    _(
                        "You have already reviewed '%(course_name)s'. You can <a href='%(review_url)s'>view your existing review</a> or <a href='%(edit_url)s'>edit it</a>."
                    )
                    % {
                        "course_name": course_name,
                        "review_url": existing_review.first().get_absolute_url(),
                        "edit_url": django.urls.reverse(
                            "reviews:review_update", kwargs={"pk": existing_review.first().pk}
                        ),
                    }
                )

        return cleaned_data
