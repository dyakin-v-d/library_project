from rest_framework import serializers
from .models import Book, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    # Добавим название категории текстом для удобства фронтенда
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'category_name', 'isbn', 'publication_year', 'is_available']