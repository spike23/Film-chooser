from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, UpdateView

from chooser.models import FilmsBase
from .forms import PremieresPeriodForm
from .models import PremierList


class PremieresScrapperView(TemplateView):
    template_name = 'premieres/premieres_list.html'
    form = PremieresPeriodForm()

    context = {
        'form': form
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


@login_required
def premieres_collector(request):
    current_user = request.user.id
    form = PremieresPeriodForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        PremierList.objects.all().filter(user_id=current_user).delete()
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')
        quote_page = 'http://www.kinofilms.ua/afisha/ukr_premieres/?month={month}&year={year}'.format(month=month,
                                                                                                      year=year)
        try:
            page = urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            name_box = soup.findAll('a', attrs={'class': 'o'})

            for film in name_box:
                title = film.text.strip()
                link = 'http://www.kinofilms.ua' + film.get('href')
                PremierList(films=title, links=link, user_id=current_user).save()
            return redirect('premieres_shower')
        except HTTPError as e:
            return HttpResponse(e.fp.read())


class PremieresShowerView(ListView):
    model = PremierList
    template_name = 'premieres/save_premieres.html'
    context_object_name = 'premieres'

    def get_queryset(self):
        films = PremierList.objects.filter(user_id=self.request.user).order_by('films')
        paginator = Paginator(films, 10)
        page = self.request.GET.get('page')
        film_list = paginator.get_page(page)
        return film_list


class SaveFilmsBase(UpdateView):
    model = PremierList

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user.id
        values = request.POST.getlist('save')
        films = PremierList.objects.filter(pk__in=values, user_id=current_user).values('films')
        for film in films:
            FilmsBase.objects.update_or_create(films=film.get('films'), user_id=current_user)

        saved_films = [film.get('films') for film in films]

        request.session['saved_films'] = saved_films
        return redirect('base_film_list')


class SearchPremieresView(ListView):
    model = PremierList
    template_name = 'films/search_film_filter.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = PremierList.objects.filter(
            Q(films__icontains=query)
        )

        return object_list
