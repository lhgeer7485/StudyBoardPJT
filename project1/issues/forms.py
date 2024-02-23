from django import forms
from .models import Issue, Comment


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ('user', 'like_users','count')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_content',)
