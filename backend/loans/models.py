from django.db import models
from django.conf import settings
from books.models import Book
from datetime import timedelta
from django.utils import timezone

class Loan(models.Model):
    # Варианты статусов
    STATUS_CHOICES = [
        ('reserved', 'Забронирована'), # Студент нажал кнопку
        ('issued', 'На руках'),       # Библиотекарь выдал
        ('returned', 'Возвращена'),   # Книга вернулась в библиотеку
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Читатель")
    
    # Когда была создана запись (бронь или выдача)
    loan_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    
    # Срок возврата теперь может быть пустым (пока книга только в брони)
    return_deadline = models.DateField(verbose_name="Срок возврата", null=True, blank=True)
    
    # Вместо BooleanField используем CharField со списком статусов
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='reserved', 
        verbose_name="Статус"
    )

    def save(self, *args, **kwargs):
        # Если это не новая запись, проверяем изменение статуса
        if self.pk:
            old_status = Loan.objects.get(pk=self.pk).status
            # Если статус изменился на "Возвращена"
            if old_status != 'returned' and self.status == 'returned':
                self.book.is_available = True
                self.book.save()
            # На случай, если книгу выдали обратно вручную (из 'returned' в 'issued')
            elif old_status == 'returned' and self.status != 'returned':
                self.book.is_available = False
                self.book.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.book.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Запись о выдаче'
        verbose_name_plural = 'Журнал выдачи'