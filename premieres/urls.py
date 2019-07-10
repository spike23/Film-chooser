from django.urls import path

from . import views

urlpatterns = [
    path('premieres-list/', views.premieres_scrapper, name='premieres_scrapper'),
    path('get-premier-list', views.premieres_collector, name='premieres_collector'),
    path('save-premieres', views.save_films_base, name='save_films_base'),
    path('show-premier-list', views.premieres_shower, name='premieres_shower')
]
