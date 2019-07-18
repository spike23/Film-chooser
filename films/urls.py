from django.urls import path

from films.views import SearchFilmsBaseView, SearchFilmsWatchingView, SearchMainView
from . import views

urlpatterns = [
    path('film-list/', views.base_film_list, name='base_film_list'),
    path('watching-list/', views.watching_film_list, name='watching_film_list'),
    path('add-list-base/', views.add_new_film, name='add_new_film'),
    path('edit-film/<int:pk>/', views.edit_film, name='edit_film'),
    path('delete-list-base/', views.delete_films_base, name='delete_films_base'),
    path('delete-list-watching/', views.delete_films_watching, name='delete_films_watching'),
    path('film-list-search/', SearchFilmsBaseView.as_view(), name='search_film_base_results'),
    path('film-watching-search/', SearchFilmsWatchingView.as_view(), name='search_film_watching_results'),
    path('film-search/', SearchMainView.as_view(), name='search_results')
]
