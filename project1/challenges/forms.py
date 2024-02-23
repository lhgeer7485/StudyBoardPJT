from django import forms
from .models import Challenge, Code

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ('problem',)
        labels = {
            'problem' : '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-floating mb-3', 'placeholder':'문제의 제목을 입력하시오.'}),
            'problem': forms.TextInput(attrs={'class': 'form-control form-floating mb-3', 'placeholder':'문제 번호(숫자만)'}),
        }

class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('content',)
        widgets = {
            'content' : forms.Textarea(attrs={'id':'editor'})
        }