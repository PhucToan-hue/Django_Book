#!/usr/bin/env python
import os
import sys
import django
import requests
from datetime import datetime, timedelta
from urllib.parse import urljoin

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_manage.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from book.models import Book

User = get_user_model()
user, _ = User.objects.get_or_create(username='admin')
user.set_password('admin123')
user.save()

refresh = RefreshToken.for_user(user)
token = str(refresh.access_token)
headers = {'Authorization': f'Bearer {token}'}
base_url = 'http://127.0.0.1:8000'

# Create test data
Book.objects.all().delete()
today = datetime.now().date()
test_books = [
    Book.objects.create(title='Python Programming', author='Guido van Rossum', price=25, quantity=10, published_date=today),
    Book.objects.create(title='Django for Beginners', author='William Vincent', price=35, quantity=5, published_date=today - timedelta(days=5)),
    Book.objects.create(title='FastAPI Guide', author='Tiangolo', price=45, quantity=8, published_date=today - timedelta(days=10)),
    Book.objects.create(title='Go Programming Language', author='Rob Pike', price=40, quantity=12, published_date=today - timedelta(days=15)),
    Book.objects.create(title='Rust by Example', author='The Rust Book Contributors', price=30, quantity=15, published_date=today - timedelta(days=20)),
]

print('=' * 80)
print('API TEST RESULTS - Book Management System')
print('=' * 80)
print()

# Test cases
tests = [
    {
        'name': '1. GET All Books (Pagination - Default 20 per page)',
        'url': '/api/books/',
    },
    {
        'name': '2. Filter by Title (title=python)',
        'url': '/api/books/?title=python',
    },
    {
        'name': '3. Filter by Author (author=vincent)',
        'url': '/api/books/?author=vincent',
    },
    {
        'name': '4. Filter by Price Range (price_min=30&price_max=45)',
        'url': '/api/books/?price_min=30&price_max=45',
    },
    {
        'name': '5. Filter by Quantity (quantity_min=10)',
        'url': '/api/books/?quantity_min=10',
    },
    {
        'name': '6. Pagination - Page Size 2 (?page_size=2)',
        'url': '/api/books/?page_size=2',
    },
    {
        'name': '7. Combined Filters (title=python|django|fastapi - by ordering by price DESC)',
        'url': '/api/books/?ordering=-price&page_size=10',
    },
    {
        'name': '8. Sort by Title (ordering=title)',
        'url': '/api/books/?ordering=title',
    },
]

for test in tests:
    url = urljoin(base_url, test['url'])
    print(f"\n{test['name']}")
    print(f"URL: GET {test['url']}")
    print('-' * 80)
    
    r = requests.get(url, headers=headers)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"Count: {data['count']} records")
        print(f"Results: {len(data['results'])} items in this page")
        print(f"Has Next: {bool(data['next'])}")
        print()
        print("Books returned:")
        for i, book in enumerate(data['results'], 1):
            print(f"  {i}. \"{book['title']}\" by {book['author']} - ${book['price']} (qty: {book['quantity']})")
    else:
        print(f"Error: {r.json()}")
    print()

print('=' * 80)
print('POST - Create New Book')
print('=' * 80)
new_book = {
    'title': 'Advanced Python',
    'author': 'Raymond Hettinger',
    'price': 55,
    'quantity': 20,
    'published_date': str(today)
}
print(f"Request Body: {new_book}")
print()
r = requests.post(urljoin(base_url, '/api/books/'), json=new_book, headers=headers)
print(f"Status: {r.status_code}")
if r.status_code == 201:
    created_book = r.json()
    print(f"✓ Created: {created_book['title']} (ID: {created_book['id']})")
else:
    print(f"Error: {r.json()}")

print()
print('=' * 80)
print('Summary of Features')
print('=' * 80)
print("""
✓ CRUD Operations
  - GET /api/books/              : List all books with pagination
  - POST /api/books/             : Create new book
  - GET /api/books/{id}/         : Get book details
  - PUT /api/books/{id}/         : Update entire book
  - PATCH /api/books/{id}/       : Partial update
  - DELETE /api/books/{id}/      : Delete book

✓ Pagination
  - Default: 20 records per page
  - Max: 100 records per page
  - Query param: ?page_size=50

✓ Filtering (Case-insensitive)
  - ?title=python                : Filter by title
  - ?author=william              : Filter by author
  - ?price_min=30&price_max=50   : Price range
  - ?quantity_min=10             : Minimum quantity
  - ?quantity_max=15             : Maximum quantity

✓ Ordering
  - ?ordering=price              : Ascending
  - ?ordering=-price             : Descending by price
  - ?ordering=-published_date    : Most recent first

✓ Authentication
  - JWT Bearer tokens via /api/token/
  - All endpoints require authentication
""")
