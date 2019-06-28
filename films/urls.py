from django.urls import path

from . import views

urlpatterns = [
    path('film-list/', views.base_film_list, name='base_film_list'),
    path('watching-list/', views.watching_film_list, name='watching_film_list'),
    path('add-list-base/', views.add_new_film, name='add_new_film'),
    path('edit-film/<int:pk>/', views.edit_film, name='edit_film'),
    path('delete-list-base/', views.delete_films_base, name='delete_films_base'),
    path('delete-list-watching/', views.delete_films_watching, name='delete_films_watching'),
]
