from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Category
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets  # ДОБАВЛЕНО fields и widgets

class BookResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=widgets.ForeignKeyWidget(Category, 'name')
    )

    class Meta:
        model = Book
        # Убедись, что publication_year есть в списке полей для обработки
        fields = ('title', 'author', 'category', 'publication_year')
        import_id_fields = ('title', 'author')

    def before_import_row(self, row, **kwargs):
        # Если года нет, ставим 2024
        if not row.get('publication_year'):
            row['publication_year'] = 2024
            
        # ОБЯЗАТЕЛЬНО: Если ISBN нет в Excel, явно ставим None (null)
        # Это предотвратит ошибку уникальности пустых строк
        if not row.get('isbn'):
            row['isbn'] = None

        # Создание категории, если её нет
        cat_name = row.get('category')
        if cat_name:
            Category.objects.get_or_create(name=cat_name)

# 2. Единый класс админки для книг
@admin.register(Book)
class BookAdmin(ImportExportModelAdmin): # Наследуемся от ImportExportModelAdmin
    resource_class = BookResource
    
    # Отображение в списке
    list_display = ('title', 'author', 'category', 'is_available_status')
    list_filter = ('is_available', 'category')
    search_fields = ('title', 'author')
    
    # Быстрое добавление: кнопка "Сохранить как новую" в карточке книги
    save_as = True
    
    # Автоматическое создание slug или других полей (если нужно) можно добавить тут

    # Метод для красивого отображения статуса (зеленый/красный)
    def is_available_status(self, obj):
        color = 'green' if obj.is_available else 'red'
        text = 'Свободна' if obj.is_available else 'Занята/Бронь'
        return format_html('<b style="color: {};">{}</b>', color, text)
    
    is_available_status.short_description = 'Доступность'

# 3. Админка для категорий
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)