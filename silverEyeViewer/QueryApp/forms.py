
from django import forms

class AnalysisForm(forms.Form):
    data = forms.CharField(label='data', max_length=100)