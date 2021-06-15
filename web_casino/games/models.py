from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy

from .funtions import bj_count


class Games(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to="images/%Y/%m/%d/", blank=True, verbose_name="Изображение")
    rules = models.TextField(blank=True, verbose_name='Правила')
    payouts = models.TextField(blank=True, verbose_name='Выплаты')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game', kwargs={'slug_game': self.slug})

    class Meta:
        verbose_name = 'Игры'
        verbose_name_plural = 'Игры'
        ordering = ['-time_update', 'name']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории Игр'
        verbose_name_plural = 'Категории Игр'
        ordering = ['name']


class Hand(models.Model):
    first_card = models.CharField(max_length=20, verbose_name='Первая Карта')
    second_card = models.CharField(max_length=20, verbose_name='Вторая Карта')
    dealer_card = models.CharField(max_length=20, verbose_name='Карта Дилера')
    decision = models.CharField(max_length=20, verbose_name='Решение Помощника')
    time_hand = models.DateTimeField(auto_now_add=True, verbose_name='Время Раздачи')
    win_result = models.CharField(max_length=10, default='Win')
    played_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwarg):
        self.decision = bj_count(self.first_card, self.second_card, self.dealer_card)
        super(Hand, self).save(*args, **kwarg)

    def get_absolute_url(self):
        return reverse_lazy('bj_result', kwargs={'pk': self.pk})