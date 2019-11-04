from django import forms
from .models import NewspaperURL, ExportPDF

class NewspaperURL(forms.ModelForm):
    class Meta:
        model = NewspaperURL
        exclude = ['enter_url']
        fields = [
            'enter_url'
        ]

class ExportPDF(forms.ModelForm):
    class Meta:
        model = ExportPDF
        exclude = ['export_pdf']
        fields = [
            'export_pdf'
        ]