from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, PasswordInput
from django import forms

from users.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username_input',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password_input',
        'placeholder': 'Input your password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password_input',
        'placeholder': 'Confirm your password',
    }))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

    def clean_password(self):
        return make_password(self.cleaned_data['password'])


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password": PasswordInput(),
        }


class ProfileForm(UserChangeForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': "custom-file-input",
    }))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "image"]
