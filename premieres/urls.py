from django.contrib.auth.decorators import login_required
from django.urls import path

from premieres.views import (SearchPremieresView, PremieresShowerView, PremieresScrapperView, SaveFilmsBase,
                             PremieresCollector)

urlpatterns = [
    path('premieres-list/', PremieresScrapperView.as_view(), name='premieres_scrapper'),
    path('get-premier-list', login_required(PremieresCollector.as_view()), name='premieres_collector'),
    path('save-premieres', login_required(SaveFilmsBase.as_view()), name='save_films_base'),
    path('show-premier-list', login_required(PremieresShowerView.as_view()), name='premieres_shower'),
    path('film-watching-search/', SearchPremieresView.as_view(), name='search_premieres_results')

]
