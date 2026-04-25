from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False) # Роль: библиотекарь или нет
    
    def __str__(self):
        return self.username