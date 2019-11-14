from django.contrib.auth.decorators import login_required
from django.urls import path

from chooser.views import AboutSiteView, BaseFilmsUploader, ChooserView

urlpatterns = [
    path('chooser', login_required(ChooserView.as_view()), name='chooser'),
    path('upload-csv/', login_required(BaseFilmsUploader.as_view()), name='base_films_uploader'),
    path('about-site/', AboutSiteView.as_view(), name='about_site')
]
