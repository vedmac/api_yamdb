from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.aggregates import Avg
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    role = models.CharField(
        max_length=10, choices=Roles.choices, default=Roles.USER)
    bio = models.CharField(max_length=320, blank=True)

    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    def is_admin(self):
        return self.role == self.Roles.ADMIN


class Genres(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='title'
    )

    def get_rating(self):
        return Review.objects.filter(title=self).aggregate(Avg('score'))

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Titles, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата отзыва',
                                    auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
],
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    title = models.ForeignKey(Review, on_delete=models.CASCADE,
                              related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text
