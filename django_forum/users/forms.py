import django.conf
import django.core.exceptions
import django.utils.timezone
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import UserProfile

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "username"]

        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "your_email@example.com"}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repeat the password'
        })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username or email'
        })

        # Customize the password field
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "bio", "birthday"]
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop("user_instance", None)
        super().__init__(*args, **kwargs)

        if args or kwargs.get("data"):
            self.user_form = UserEditForm(data=kwargs.get("data"), instance=self.user_instance, prefix="user")
        else:
            self.user_form = UserEditForm(instance=self.user_instance, prefix="user")

    def is_valid(self):
        user_valid = self.user_form.is_valid()
        profile_valid = super().is_valid()
        return user_valid and profile_valid

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 5 * 1024 * 1024:
            raise django.forms.ValidationError("Max file size is 5MB")
        return avatar

    def save(self, *, commit=True):
        user = self.user_form.save(commit=commit)

        profile = super().save(commit=False)
        profile.user = user

        if commit:
            profile.save()

        return profile
