from django import forms

from forum.models import Answer, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "What's your question?"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Describe your problem in detail...", "rows": 5},
            ),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Write your answer here...", "rows": 4},
            ),
        }
