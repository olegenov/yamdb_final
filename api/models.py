from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import max_value_current_year, gen_confirmation_code


class CustomUser(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MODERATOR = 'moderator', _('Moderator')
        USER = 'user', _('User')

    email = models.EmailField('email', unique=True)
    password = models.CharField(blank=True, max_length=128)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
    )


class ConfirmationCode(models.Model):
    email = models.EmailField('User Email')
    valid = models.BooleanField('Code Valid', default=True)
    code = models.IntegerField(
        'Confirmation code',
        default=gen_confirmation_code()
    )
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='code'
    )


class Title(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        'Category',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        related_name='posts'
    )
    year = models.IntegerField(
        blank=True,
        validators=[MinValueValidator(1984), max_value_current_year]
    )


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка отзыва', default=10,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        "Дата публикации", null=True, blank=True,
        auto_now_add=True
    )
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=30)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=30)

    def __str__(self):
        return self.slug
