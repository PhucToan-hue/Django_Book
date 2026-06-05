from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from book.models import Book
from book.serializers import BookListSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]