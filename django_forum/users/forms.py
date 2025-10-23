import django.conf
import django.core.exceptions
import django.utils.timezone
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from users.models import UserProfile

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "username"]

        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": _("your_email@example.com")}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Enter username")}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter your password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Repeat the password')
        })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter your username or email')
        })

        # Customize the password field
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter your password')
        })


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter your {field.replace("_", " ")}'
            })


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'birthday']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control form-control-sm', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make avatar field not required since it's blank=True
        self.fields['avatar'].required = False