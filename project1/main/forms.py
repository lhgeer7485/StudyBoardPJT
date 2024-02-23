from django import forms
from .models import Main, Comment


class MainForm(forms.ModelForm):
    class Meta:
        model = Main
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
