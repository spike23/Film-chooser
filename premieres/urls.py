from django.contrib.auth.decorators import login_required
from django.urls import path

from premieres.views import SearchPremieresView, PremieresShowerView
from . import views

urlpatterns = [
    path('premieres-list/', views.premieres_scrapper, name='premieres_scrapper'),
    path('get-premier-list', views.premieres_collector, name='premieres_collector'),
    path('save-premieres', views.save_films_base, name='save_films_base'),
    path('show-premier-list', login_required(PremieresShowerView.as_view()), name='premieres_shower'),
    path('film-watching-search/', SearchPremieresView.as_view(), name='search_premieres_results')

]
