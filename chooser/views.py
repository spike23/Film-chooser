import csv
import io
import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .forms import FilmsForm
from .models import FilmsBase, FilmsToWatching

main_page_template = 'index.html'
film_list_template = 'film_list.html'
watching_list_template = 'watching_list.html'


def index(request):
    current_user = request.user.id
    form = FilmsForm(current_user)
    last_list = FilmsToWatching.objects.all().filter(user_id=current_user)
    paginator = Paginator(last_list, 5)
    page = request.GET.get('page')
    film_list_latest = paginator.get_page(page)

    updated = FilmsBase.objects.latest('last_updated')

    context = {
        'form': form,
        'last_watching': film_list_latest,
        'last_updated': updated
    }
    return render(request, main_page_template, context)


@login_required
def chooser(request):
    current_user = request.user.id
    form = FilmsForm(current_user, request.POST)

    if request.method == 'POST' and form.is_valid():
        FilmsToWatching.objects.all().filter(user_id=current_user).delete()
        films_number = form.cleaned_data.get('films')
        result = random_films(films=FilmsBase.objects.filter(user_id=current_user).values_list('films', flat=True),
                              quantity=films_number)
        for film in result:
            film_watch = FilmsToWatching(films=film, user_id=current_user)
            film_watch.save()
            base_film = FilmsBase.objects.get(films=film, user_id=current_user)
            base_film.delete()

        return redirect('watching_film_list')

    context = {
        'form': form
    }

    return render(request, main_page_template, context)


def random_films(films, quantity):
    choice = random.sample(list(films), quantity)
    return choice


@login_required
def base_films_uploader(request):
    current_user = request.user.id
    form = FilmsForm(current_user)
    last_list = FilmsToWatching.objects.all().filter(user_id=current_user)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This file is not a .csv file')
    data = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data)
    count = 0
    for film in csv.reader(io_string):
        _, created = FilmsBase.objects.update_or_create(
            films=film[0],
            last_updated=datetime.now().strftime("%Y-%m-%d"),
            user_id=current_user
        )
        count += 1

    context = {
        'form': form,
        'counter': count,
        'last_watching': last_list,
    }

    return render(request, main_page_template, context)


@login_required
def base_film_list(request):
    current_user = request.user.id
    films = FilmsBase.objects.filter(user_id=current_user).values_list('films', flat=True)
    paginator = Paginator(films, 7)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)

    context = {
        'films': film_list
    }
    
    return render(request, film_list_template, context)


@login_required
def watching_film_list(request):
    current_user = request.user.id
    films = FilmsToWatching.objects.all().filter(user_id=current_user)
    paginator = Paginator(films, 7)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)

    context = {
        'films': film_list
    }

    return render(request, watching_list_template, context)
