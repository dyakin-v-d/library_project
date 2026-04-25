from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Кабинет Библиотекаря СКФУ"  # Заголовок в синей шапке
admin.site.site_title = "Библиотека СКФУ"             # Текст на вкладке браузера
admin.site.index_title = "Панель управления фондом"   # Текст на главной странице админки

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
    path('api/loans/', include('loans.urls')),  # Добавляем это
    # Пути для авторизации теперь будут api/auth/...
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]