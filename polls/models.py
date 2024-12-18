import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    last_name = models.CharField(max_length=254, verbose_name="Фамилия")
    first_name = models.CharField(max_length=254, verbose_name="Имя")
    email = models.EmailField(max_length=254, verbose_name="Почта", unique=True)
    username = models.CharField(max_length=254, verbose_name="Логин", unique=True)
    password = models.CharField(max_length=254, verbose_name="Пароль")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    lifetime = models.DurationField(default=timedelta(days=7))
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')
