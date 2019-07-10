from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from chooser.models import FilmsBase
from .forms import PremieresPeriodForm
from .models import PremierList

premieres_template = 'premieres/premieres_list.html'
save_premieres_template = 'premieres/save_premieres.html'


def premieres_scrapper(request):
    form = PremieresPeriodForm()
    context = {
        'form': form
    }

    return render(request, premieres_template, context)


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
        page = urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.findAll('a', attrs={'class': 'o'})

        for film in name_box:
            title = film.text.strip()
            link = 'http://www.kinofilms.ua' + film.get('href')
            PremierList(films=title, links=link, user_id=current_user).save()
        return redirect('premieres_shower')


@login_required
def premieres_shower(request):
    current_user = request.user.id
    films = PremierList.objects.filter(user_id=current_user).order_by('films')
    paginator = Paginator(films, 10)
    page = request.GET.get('page')
    film_list = paginator.get_page(page)

    context = {
        'premieres': film_list,
    }

    return render(request, save_premieres_template, context)


@login_required
def save_films_base(request):
    current_user = request.user.id
    values = request.POST.getlist('save')
    films = PremierList.objects.filter(pk__in=values, user_id=current_user).values('films')
    for film in films:
        FilmsBase.objects.update_or_create(films=film.get('films'), user_id=current_user)

    saved_films = [film.get('films') for film in films]

    request.session['saved_films'] = saved_films

    return redirect('base_film_list')
