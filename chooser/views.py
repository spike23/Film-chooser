import random

from django.shortcuts import render, redirect
from .forms import FilmsForm
from .models import FilmsBase, FilmsToWatching


template_name = 'index.html'


def index(request):
    form = FilmsForm()
    last_list = FilmsToWatching.objects.all()
    context = {
        'form': form,
        'last_watching': last_list
    }
    return render(request, template_name, context)


def chooser(request):
    last_list = FilmsToWatching.objects.all()
    count_list = FilmsBase.objects.count()

    if request.method == 'POST':
        FilmsToWatching.objects.all().delete()
        form = FilmsForm(request.POST)
        if form.is_valid():
            films_number = form.cleaned_data.get('films')
            result = random_films(films=FilmsBase.objects.values('films'), quantity=films_number)
            for film in result:
                film_watch = FilmsToWatching(films=film)
                film_watch.save()
                base_film = FilmsBase.objects.get(films=film)
                base_film.delete()
            random_list = FilmsToWatching.objects.all()

            context = {
                'form': form,
                'chooser': random_list,
                'last_watching': last_list
            }

            return render(request, template_name, context)
    return redirect('index')
    # TODO Validation of films number, removing or not film from base


def random_films(films, quantity):
    choice = random.sample(list(films), quantity)
    result_list = [film.get('films') for film in choice]
    return result_list
