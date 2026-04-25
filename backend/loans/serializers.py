from rest_framework import serializers
from .models import Loan
from books.models import Book

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Loan
        fields = ['id', 'book', 'book_title', 'user', 'username', 'loan_date', 'return_deadline', 'is_returned']