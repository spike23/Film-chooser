import csv
import io
import random
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView

from .forms import FilmsForm
from .models import FilmsBase, FilmsToWatching


class IndexView(ListView):
    model = FilmsBase, FilmsToWatching
    template_name = 'chooser/index.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user.id
        form = FilmsForm(current_user)
        last_list = FilmsToWatching.objects.all().filter(user_id=current_user).order_by('films')
        paginator = Paginator(last_list, 5)
        page = request.GET.get('page')
        film_list_latest = paginator.get_page(page)

        if FilmsBase.objects.filter(user_id=current_user):
            updated = FilmsBase.objects.filter(user_id=current_user).latest('last_updated')
        else:
            updated = None

        context = {
            'form': form,
            'last_watching': film_list_latest,
            'last_updated': updated
        }
        return render(request, self.template_name, context)


class ChooserView(ListView):
    template_name = 'chooser/index.html'
    model = FilmsToWatching

    @staticmethod
    def random_films(films, quantity):
        choice = random.sample(list(films), quantity)
        return choice

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user.id
        form = FilmsForm(current_user, request.POST)

        if request.method == 'POST' and form.is_valid():
            FilmsToWatching.objects.all().filter(user_id=current_user).delete()
            films_number = form.cleaned_data.get('films')
            result = self.random_films(
                films=FilmsBase.objects.filter(user_id=current_user).values_list('films', flat=True),
                quantity=films_number)
            for film in result:
                film_watch = FilmsToWatching(films=film, user_id=current_user)
                film_watch.save()

            return redirect('watching_film_list')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class BaseFilmsUploader(UpdateView):
    template_name = 'chooser/index.html'
    model = FilmsBase, FilmsToWatching

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user.id
        form = FilmsForm(current_user)
        last_list = FilmsToWatching.objects.all().filter(user_id=current_user)
        updated = FilmsBase.objects.latest('last_updated')

        text_file = request.FILES['file']

        if not text_file.name.endswith('.csv') and not text_file.name.endswith('.txt'):
            context = {
                'form': form,
                'last_watching': last_list,
                'last_updated': updated,
                'error': True
            }
            return render(request, self.template_name, context)

        data = text_file.read().decode('utf-8')
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
            'last_updated': updated
        }

        return render(request, self.template_name, context)


class AboutSiteView(DetailView):
    template_name = 'chooser/about_site.html'

    def dispatch(self, request, *args, **kwargs):
        return render(self.request, self.template_name)
