from django import forms
from django.forms import ModelForm
from profanity_check import predict

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


