from django.urls import path

from . import views

urlpatterns = [
    path('premiers-list/', views.premiers_scrapper, name='premiers_scrapper'),

]
