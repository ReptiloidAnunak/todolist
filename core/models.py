from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    birthdate = models.DateField(null=True)
    image = models.ImageField(null=True, blank=True, upload_to='users_avatars')

    def __str__(self):
        self.username
