from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Loan
from books.models import Book
from .serializers import LoanSerializer
from datetime import date, timedelta


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_librarian:
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user, is_returned=False)

    @action(detail=False, methods=['post'], url_path='rent/(?P<book_id>[0-9]+)')
    def rent(self, request, book_id=None):
        book = Book.objects.filter(id=book_id, is_available=True).first()

        if not book:
            return Response(
                {"error": "Книга недоступна"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Loan.objects.create(
            user=request.user,
            book=book,
            return_deadline=date.today() + timedelta(days=14)
        )

        book.is_available = False
        book.save()

        return Response(
            {"message": "Книга успешно взята"},
            status=status.HTTP_201_CREATED
        )