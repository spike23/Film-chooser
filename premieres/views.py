from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from chooser.models import FilmsBase

premiers_template = 'premiers_list.html'


def premiers_scrapper(request):
    quote_page = 'http://www.kinofilms.ua/afisha/ukr_premieres/?month=06&year=2019'
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.findAll('a', attrs={'class': 'o'})

    # premier_films = dict(enumerate(i.text.strip() for i in name_box))

    premier_films = [title.text.strip() for title in name_box]
    paginator = Paginator(premier_films, 7)
    page = request.GET.get('page')
    premiers_list = paginator.get_page(page)

    links = ['http://www.kinofilms.ua' + link.get('href') for link in name_box]
    # TODO https://stackoverflow.com/questions/2067006/accessing-a-dict-by-variable-in-django-templates
    for link in links:
        context = {
            'premiers': premiers_list,
            'movie_page': link
        }

        return render(request, premiers_template, context)


def save_films_base(request):
    current_user = request.user.id
    values = request.POST.getlist('save')
    # FilmsBase.objects.filter(pk__in=values, user_id=current_user).save()
    # FilmsBase.objects.update_or_create(films=film, user_id=current_user)
    # return redirect('premiers_scrapper')
    return HttpResponse('{}'.format(values))
