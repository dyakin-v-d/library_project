from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название книги")
    author = models.CharField(max_length=255, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name="Жанр")
    # null=True позволяет хранить "ничего" без конфликтов уникальности
    isbn = models.CharField("ISBN", max_length=13, unique=True, null=True, blank=True)
    publication_year = models.IntegerField("Год издания", null=True, blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Доступна")

    def __str__(self):
        return f"{self.title} — {self.author}"
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'