from django.db import models


class FilmsBase(models.Model):
    films = models.CharField(max_length=100)

    def __str__(self):
        return '{films}'.format(films=self.films)


class FilmsToWatching(models.Model):
    films = models.CharField(max_length=100)

    def __str__(self):
        return '{films}'.format(films=self.films)
