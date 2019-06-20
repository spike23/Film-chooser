from django.db import models


class FilmsBase(models.Model):
    films = models.CharField(max_length=100)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return '{films}, {last_updated}'.format(films=self.films, last_updated=self.last_updated)


class FilmsToWatching(models.Model):
    films = models.CharField(max_length=100)

    def __str__(self):
        return '{films}'.format(films=self.films)
