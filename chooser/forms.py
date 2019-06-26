from django import forms

from chooser.models import FilmsBase


class FilmsForm(forms.Form):

    films = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity of films to watching'}),
        min_value=1, )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FilmsForm, self).__init__(*args, **kwargs)

    def clean_films(self):
        films = self.cleaned_data['films']
        if FilmsBase.objects.filter(user_id=self.user).count() < films:
            raise forms.ValidationError('You choose value that larger than you have in your film list.')

        return films


class NewFilmForm(forms.Form):

    new_film = forms.CharField()  # (label='New film', max_length=100)
