import csv
import io
import random

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .forms import FilmsForm
from .models import FilmsBase, FilmsToWatching

template_name = 'index.html'


def index(request):
    current_user = request.user.id
    form = FilmsForm()
    last_list = FilmsToWatching.objects.all()
    updated = FilmsBase.objects.latest('last_updated')
    context = {
        'form': form,
        'last_watching': last_list,
        'last_updated': updated
    }
    return render(request, template_name, context)


@login_required
def chooser(request):
    current_user = request.user.id
    if request.method == 'POST':
        FilmsToWatching.objects.all().filter(user_id=current_user).delete()
        form = FilmsForm(request.POST)
        if form.is_valid():
            films_number = form.cleaned_data.get('films')
            result = random_films(films=FilmsBase.objects.filter(user_id=current_user).values_list('films', flat=True),
                                  quantity=films_number)
            for film in result:
                film_watch = FilmsToWatching(films=film, user_id=current_user)
                film_watch.save()
                base_film = FilmsBase.objects.get(films=film, user_id=current_user)
                base_film.delete()
            random_list = FilmsToWatching.objects.all()

            context = {
                'form': form,
                'chooser': random_list,
            }

            return render(request, template_name, context)
    return redirect('index')


def random_films(films, quantity):
    choice = random.sample(list(films), quantity)
    return choice


def base_films_uploader(request):
    current_user = request.user.id

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This file is not a .csv file')
    data = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data)

    for film in csv.reader(io_string):
        _, created = FilmsBase.objects.update_or_create(
            films=film[0],
            last_updated=datetime.now().strftime("%Y-%m-%d"),
            user_id=current_user
        )

    return redirect('chooser')
