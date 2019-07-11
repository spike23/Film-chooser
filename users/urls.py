from django.urls import path
from .views import change_password, SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('change-password/', change_password, name='change_password'),
]