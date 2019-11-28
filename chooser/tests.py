import csv
import random
from datetime import datetime

import pytest
from django.urls import reverse

from chooser.models import FilmsBase, FilmsToWatching
from chooser.views import ChooserView


class TestChooser:

    @staticmethod
    def user_base_prepare(django_user_model, tmpdir):
        data = """test_film
                  film_test"""
        user = django_user_model.objects.create(
            username='anonymous', password='secret'
        )
        with open(tmpdir.join('test.csv'), 'w') as test_file:
            test_file.writelines(data)

        with open(tmpdir.join('test.csv'), 'r') as f:
            reader = csv.reader(f)
            for film in reader:
                print(film[0])
                _, created = FilmsBase.objects.update_or_create(
                    films=film[0],
                    last_updated=datetime.now().strftime("%Y-%m-%d"),
                    user_id=user.id
                )
        return user

    @pytest.mark.django_db
    def test_home(self, client):
        url = reverse('base_films_uploader')
        response = client.get(url)
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_csv_loader(self, django_user_model, tmpdir):
        self.user_base_prepare(django_user_model, tmpdir)
        assert FilmsBase.objects.count() == 2

    @pytest.mark.django_db
    def test_chooser_film(self, django_user_model, tmpdir):
        user = self.user_base_prepare(django_user_model, tmpdir)

        FilmsToWatching.objects.all().filter(user_id=user.id).delete()
        films_number = 2
        result = ChooserView.random_films(
            films=FilmsBase.objects.filter(user_id=user.id).values_list('films', flat=True),
            quantity=films_number)
        for film in result:
            film_watch = FilmsToWatching(films=film, user_id=user.id)
            film_watch.save()

        assert FilmsToWatching.objects.count() == 2
