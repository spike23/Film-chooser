from django.contrib.auth.decorators import login_required
from django.urls import path

from films.views import (SearchFilmsBaseView, SearchFilmsWatchingView, SearchMainView, AddNewFilmView,
                         WatchingFilmListView, BaseFilmListView, EditFilmView, DeleteFilmsBaseView,
                         DeleteFilmsWatchingView)

urlpatterns = [
    path('film-list/', login_required(BaseFilmListView.as_view()), name='base_film_list'),
    path('watching-list/', login_required(WatchingFilmListView.as_view()), name='watching_film_list'),
    path('add-list-base/', login_required(AddNewFilmView.as_view()), name='add_new_film'),
    path('edit-film/<int:pk>/', login_required(EditFilmView.as_view()), name='edit_film'),
    path('delete-list-base/', login_required(DeleteFilmsBaseView.as_view()), name='delete_films_base'),
    path('delete-list-watching/', login_required(DeleteFilmsWatchingView.as_view()), name='delete_films_watching'),
    path('film-list-search/', SearchFilmsBaseView.as_view(), name='search_film_base_results'),
    path('film-watching-search/', SearchFilmsWatchingView.as_view(), name='search_film_watching_results'),
    path('film-search/', SearchMainView.as_view(), name='search_results')
]
