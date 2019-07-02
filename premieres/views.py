from django.shortcuts import render

premiers_template = 'premiers_list.html'


def premiers_scrapper(request):
    return render(request, premiers_template)
