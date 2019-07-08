from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import PremierList
from premieres.forms import PremiersPeriodForm

premiers_template = 'premiers_list.html'


def premiers_scrapper(request):
    form = PremiersPeriodForm()
    context = {
        'form': form
    }

    return render(request, premiers_template, context)


def premiers_collector(request):
    current_user = request.user.id
    form = PremiersPeriodForm(request.POST)
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
        return redirect('index')


def save_films_base(request):
    current_user = request.user.id
    values = request.POST.getlist('save')
    # FilmsBase.objects.filter(pk__in=values, user_id=current_user).save()
    # FilmsBase.objects.update_or_create(films=film, user_id=current_user)
    # return redirect('premiers_scrapper')
    return HttpResponse('{}'.format(values))
