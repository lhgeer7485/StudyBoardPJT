from django import forms
from .models import Plan, Comment


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude = ('user', 'like_users','count')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_content',)
