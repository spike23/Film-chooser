from django import forms

from chooser.utils import max_value_definer


class FilmsForm(forms.Form):
    films = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity of films to watching'}),
        min_value=1, max_value=max_value_definer)
