from django.db import models
from users.models import CustomUser


class FilmsBase(models.Model):
    films = models.CharField(max_length=100)
    last_updated = models.DateField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return '{films}, {last_updated}'.format(films=self.films, last_updated=self.last_updated)


class FilmsToWatching(models.Model):
    films = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return '{films}'.format(films=self.films)
