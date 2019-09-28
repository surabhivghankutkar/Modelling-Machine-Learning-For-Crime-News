from django import forms
from .models import ExportPDF

class ExportPDF(forms.ModelForm):
    class Meta:
        model = ExportPDF
        exclude = ['export_pdf']
        fields = [
            'export_pdf'
        ]
