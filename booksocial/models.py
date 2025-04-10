from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    bio = models.TextField(_('биография'), blank=True)
    avatar = models.ImageField(_('аватар'), upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')


class Book(models.Model):
    title = models.CharField(_('название'), max_length=200)
    author = models.CharField(_('автор'), max_length=100)
    genre = models.CharField(_('жанр'), max_length=50)
    description = models.TextField(_('описание'))
    cover = models.ImageField(_('обложка'), upload_to='covers/', blank=True, null=True)
    published_date = models.DateField(_('дата публикации'), null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(_('текст рецензии'))
    rating = models.PositiveSmallIntegerField(_('оценка'), choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)


class ReadingList(models.Model):
    LIST_TYPES = (
        ('WT', 'Хочу прочитать'),
        ('IP', 'В процессе'),
        ('RD', 'Прочитано'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    name = models.CharField(_('название списка'), max_length=100)
    books = models.ManyToManyField(Book, related_name='reading_lists')
    list_type = models.CharField(_('тип списка'), max_length=2, choices=LIST_TYPES)
    is_public = models.BooleanField(_('публичный список'), default=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
