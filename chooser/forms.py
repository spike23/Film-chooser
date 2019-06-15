from django import forms


class FilmsForm(forms.Form):
    films = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity of films to watching'}),
        min_value=1)
