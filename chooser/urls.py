from django.urls import path

from . import views

urlpatterns = [
    path('chooser', views.chooser, name='chooser'),
    path('upload-csv/', views.base_films_uploader, name='base_films_uploader'),
]
