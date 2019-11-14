from django.db import models

from users.models import CustomUser


class PremierList(models.Model):
    films = models.CharField(max_length=100, unique=False)
    links = models.URLField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return '{films}, {links}'.format(films=self.films, links=self.links)

    @staticmethod
    def class_name():
        return "list of premieres"
