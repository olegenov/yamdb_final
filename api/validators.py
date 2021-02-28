import datetime
from random import randint

from django.core.validators import MaxValueValidator, MinValueValidator


def max_value_current_year(value):
    return MaxValueValidator(datetime.date.today().year)(value)


def gen_confirmation_code():
    return randint(1000, 9999)
