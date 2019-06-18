from .models import FilmsBase


def max_value_definer():
    return FilmsBase.objects.count()
