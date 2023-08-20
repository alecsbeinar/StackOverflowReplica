from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, PasswordInput
from profanity_check import predict
from django.contrib.auth.models import User

from qa.models import Answer, Question


class AskForm(forms.Form):
    title = forms.CharField(max_length=80)
    text = forms.CharField(widget=forms.Textarea)
    author = None

    def clean_text(self):
        text = self.cleaned_data['text']
        if predict([text])[0]:
            raise forms.ValidationError(
                u"Message is not correct", code="incorrect"
            )
        return text

    def save(self):
        question = Question(**self.cleaned_data, author=self.author)
        question.save()
        return question


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


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
