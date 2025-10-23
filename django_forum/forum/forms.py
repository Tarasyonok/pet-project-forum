from django import forms
from django.utils.translation import gettext_lazy as _

from forum.models import Answer, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": _("What's your question?")}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": _("Describe your problem in detail..."), "rows": 5},
            ),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": _("Write your answer here..."), "rows": 4},
            ),
        }
