from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import Loan
from django.contrib.admin import SimpleListFilter

# 1. Сначала объявляем фильтр
class OverdueFilter(SimpleListFilter):
    title = 'Дедлайн'
    parameter_name = 'is_overdue'

    def lookups(self, request, model_admin):
        return (
            ('overdue', 'Просрочено'),
            ('active', 'На руках (в срок)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'overdue':
            return queryset.filter(
                status='issued', 
                return_deadline__lt=timezone.now()
            )
        if self.value() == 'active':
            return queryset.filter(
                status='issued',
                return_deadline__gte=timezone.now()
            )
        return queryset

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user', 'colored_status', 'loan_date', 'return_deadline')
    
    # 2. ПОДКЛЮЧАЕМ фильтр здесь
    list_filter = (OverdueFilter, 'status', 'loan_date')
    
    search_fields = ('book__title', 'user__username')
    actions = ['make_issued', 'make_returned']

    def colored_status(self, obj):
        # Добавим красную подсветку, если срок просрочен
        is_overdue = obj.status == 'issued' and obj.return_deadline and obj.return_deadline < timezone.now().date()
        
        if is_overdue:
            return format_html('<b style="color: #d32f2f;">🛑 ПРОСРОЧЕНО</b>')
            
        colors = {
            'reserved': '#ff9800', # Оранжевый
            'issued': '#4caf50',   # Зеленый
            'returned': '#9e9e9e', # Серый
        }
        return format_html(
            '<b style="color: {};">{}</b>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Статус'

    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Название книги'

    @admin.action(description='Выдать выбранные (на 14 дней)')
    def make_issued(self, request, queryset):
        # Ставим статус и сразу дедлайн от текущей даты
        deadline = timezone.now() + timedelta(days=14)
        updated = queryset.update(status='issued', return_deadline=deadline)
        self.message_user(request, f"Обновлено записей: {updated}. Срок возврата установлен до {deadline.strftime('%d.%m.%Y')}")

    @admin.action(description='Пометить как возвращенные')
    def make_returned(self, request, queryset):
        for loan in queryset:
            loan.status = 'returned'
            loan.save()
        self.message_user(request, "Книги успешно возвращены в фонд.")