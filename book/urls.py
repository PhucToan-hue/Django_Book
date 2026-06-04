from django.urls import path
from book import views


urlpatterns = [
    path('books', views.books, name='books'),
    path('books/<int:id>', views.book_detail, name='book-detail')
]   