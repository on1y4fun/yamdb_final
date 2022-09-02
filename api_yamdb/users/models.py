from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_yamdb.settings import ADMIN, MODERATOR, USER

CHOICES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]


class User(AbstractUser):
    """Модель User, доступны методы GET, POST, PATCH, DELETE."""

    REQUIRED_FIELDS = ['email']

    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email_address'), max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль', max_length=42, choices=CHOICES, default=CHOICES[0][0]
    )
    confirmation_code = models.CharField(max_length=32, blank=True)

    admin_methods = ('POST', 'PUT', 'PATCH', 'DELETE',)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return (self.role == ADMIN or self.is_staff) and self.is_authenticated

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
