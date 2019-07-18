from django import forms
from datetime import datetime


def current_year_validation():
    return datetime.now().year


class PremieresPeriodForm(forms.Form):

    month = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'month'}),
        min_value=1, max_value=12)

    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'year'}),
        min_value=2000, max_value=current_year_validation())
