from django import forms
from .models import NewspaperURL

class NewspaperURL(forms.ModelForm):
    class Meta:
        model = NewspaperURL
        exclude = ['enter_url']
        fields = [
            'enter_url'
        ]
