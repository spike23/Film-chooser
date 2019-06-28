"""film_chooser URL Configuration

The `urlpatterns` list routes URLs to chooser_views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function chooser_views
    1. Add an import:  from my_app import chooser_views
    2. Add a URL to urlpatterns:  path('', chooser_views.home, name='home')
Class-based chooser_views
    1. Add an import:  from other_app.chooser_views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from chooser import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('test/', views.test_view, name='test_view'),

    path('chooser/', include('chooser.urls')),
    path('films/', include('films.urls')),

    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls'))
]
