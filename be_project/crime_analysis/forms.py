from django import forms
from .models import NewspaperURL

class NewspaperURL(forms.ModelForm):
    class Meta:
        model = NewspaperURL
        fields = [
            'enter_url'
        ]
