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
from django.contrib.auth import views as auth_views
from chooser import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('chooser/', include('chooser.urls')),
    path('films/', include('films.urls')),
    path('premieres/', include('premieres.urls')),

    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

    path('password-reset',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             html_email_template_name="registration/password_reset_email.html",
             email_template_name='registration/password_reset_email.html',
             subject_template_name="registration/password_reset_subject.txt",
         ),
         name="password_reset"),

    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'),
         name="password_reset_done"),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'),
         name="password_reset_complete"),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'),
         name="password_reset_confirm"),
]
