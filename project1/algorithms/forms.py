from django import forms
from .models import Algorithm

class AlgorithmFrom(forms.ModelForm):
    class Meta:
        model=Algorithm
        fields = '__all__'
        read_only_fields = ('user','problem')
