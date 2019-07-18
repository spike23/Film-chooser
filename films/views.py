from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView

from chooser.forms import NewFilmForm
from chooser.models import FilmsBase, FilmsToWatching
from premieres.models import PremierList

film_list_template = 'films/film_list.html'
watching_list_template = 'films/watching_list.html'
edit_film_template = 'films/edit_film.html'


@login_required
def base_film_list(request):
    current_user = request.user.id
    films = FilmsBase.objects.filter(user_id=current_user).order_by('films')
    paginator = Paginator(films, 7)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)

    saved_films_premieres = request.session.get('saved_films')

    context = {
        'films': film_list,
        'saved_films': saved_films_premieres
    }

    if request.session.get('saved_films'):
        del request.session['saved_films']

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


class SearchFilmsBaseView(ListView):
    model = FilmsBase
    template_name = 'films/search_film_filter.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = FilmsBase.objects.filter(
            Q(films__icontains=query)
        )

        return object_list


class SearchFilmsWatchingView(ListView):
    model = FilmsToWatching
    template_name = 'films/search_film_filter.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = FilmsToWatching.objects.filter(
            Q(films__icontains=query)
        )

        return object_list


class SearchMainView(ListView):
    template_name = 'chooser/common_search_filter.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            film_base = FilmsBase.objects.filter(
            Q(films__icontains=query)
        )
            watching_film = FilmsToWatching.objects.filter(
            Q(films__icontains=query)
        )
            premieres = PremierList.objects.filter(
            Q(films__icontains=query)
        )
            queryset_chain = chain(
                film_base,
                watching_film,
                premieres
            )
            return queryset_chain
