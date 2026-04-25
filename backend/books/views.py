from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from loans.models import Loan
from .models import Book, Category 
from .serializers import BookSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']

    # 1. МЕТОД ДЛЯ БРОНИРОВАНИЯ
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rent(self, request, pk=None):
        book = self.get_object()
        
        if not book.is_available:
            return Response(
                {'error': 'Книга уже занята или забронирована'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем запись с явным статусом 'reserved'
        Loan.objects.create(
            user=request.user, 
            book=book,
            status='reserved' # Указываем, что это именно бронь
        )
        
        book.is_available = False
        book.save()
        
        return Response({'status': 'Книга забронирована! Заберите её в течение 2-х дней.'}, status=status.HTTP_200_OK)

    # 2. МЕТОД ДЛЯ ЛИЧНОГО КАБИНЕТА (теперь внутри класса!)
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_loans(self, request):
        # Получаем все активные записи (бронь + выданные)
        loans = Loan.objects.filter(user=request.user).exclude(status='returned')
        
        data = [{
            'id': loan.id,
            'book_title': loan.book.title,
            'author': loan.book.author, # Добавил автора для красоты в ЛК
            'status': loan.status, # Вернет 'reserved' или 'issued'
            'date': loan.loan_date.strftime('%d.%m.%Y'),
            'deadline': loan.return_deadline.strftime('%d.%m.%Y') if loan.return_deadline else None
        } for loan in loans]
        
        return Response(data)