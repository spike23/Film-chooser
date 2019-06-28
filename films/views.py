from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from chooser.forms import NewFilmForm
from chooser.models import FilmsBase, FilmsToWatching

film_list_template = 'film_list.html'
watching_list_template = 'watching_list.html'
edit_film_template = 'edit_film.html'


@login_required
def base_film_list(request):
    current_user = request.user.id
    films = FilmsBase.objects.filter(user_id=current_user).order_by('films')
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
    films = FilmsToWatching.objects.filter(user_id=current_user).order_by('films')
    paginator = Paginator(films, 7)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)

    context = {
        'films': film_list
    }

    return render(request, watching_list_template, context)


@login_required
def delete_films_base(request):
    current_user = request.user.id
    values = request.POST.getlist('delete')
    FilmsBase.objects.filter(pk__in=values, user_id=current_user).delete()
    return redirect('base_film_list')


@login_required
def delete_films_watching(request):
    current_user = request.user.id
    values = request.POST.getlist('delete')
    FilmsToWatching.objects.filter(pk__in=values, user_id=current_user).delete()
    return redirect('watching_film_list')


@login_required
def add_new_film(request):
    current_user = request.user.id
    form = NewFilmForm(request.POST)
    films = FilmsBase.objects.filter(user_id=current_user).order_by('films')
    paginator = Paginator(films, 7)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)
    if request.method == 'POST' and form.is_valid():
        film = form.cleaned_data.get('new_film')
        FilmsBase.objects.update_or_create(films=film, user_id=current_user)

        context = {
            'form': form,
            'new_film': film,
            'films': film_list
        }

        return render(request, film_list_template, context)


@login_required
def edit_film(request, pk):
    current_user = request.user.id
    form = NewFilmForm(request.POST)
    edited = FilmsBase.objects.get(user_id=current_user, pk=pk)

    films = FilmsBase.objects.filter(user_id=current_user).order_by('films')
    paginator = Paginator(films, 7)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)

    if request.method == 'POST' and form.is_valid():
        film = form.cleaned_data.get('new_film')
        edited.films = film
        edited.save()

    context = {
        'film': edited,
        'films': film_list
    }

    return render(request, edit_film_template, context)
