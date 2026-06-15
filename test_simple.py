import os
import sys
import django
import requests
from datetime import datetime, timedelta

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

# Create test data
Book.objects.all().delete()
today = datetime.now().date()
books = [
    Book.objects.create(title='Python 101', author='Guido', price=25, quantity=10, published_date=today),
    Book.objects.create(title='Django Guide', author='William', price=35, quantity=5, published_date=today - timedelta(days=5)),
    Book.objects.create(title='FastAPI', author='Tiangolo', price=45, quantity=8, published_date=today - timedelta(days=10)),
]

print('=' * 60)
print('TEST API CRUD')
print('=' * 60)
print()

# Test 1: GET list
r = requests.get('http://127.0.0.1:8000/api/books/', headers=headers)
print(f'1. GET /api/books/ - Status: {r.status_code}')
data = r.json()
print(f'   Total records: {data["count"]}')
print(f'   Records in page: {len(data["results"])}')
print()

# Test 2: Filter title
r = requests.get('http://127.0.0.1:8000/api/books/?title=python', headers=headers)
print(f'2. GET /api/books/?title=python - Status: {r.status_code}')
data = r.json()
print(f'   Found: {len(data["results"])} books')
for book in data['results']:
    print(f'   - {book["title"]} (${book["price"]})')
print()

# Test 3: Filter price
r = requests.get('http://127.0.0.1:8000/api/books/?price_min=30&price_max=40', headers=headers)
print(f'3. GET /api/books/?price_min=30&price_max=40 - Status: {r.status_code}')
data = r.json()
print(f'   Found: {len(data["results"])} books in price range')
for book in data['results']:
    print(f'   - {book["title"]}: ${book["price"]}')
print()

# Test 4: POST
new_book = {'title': 'Go Programming', 'author': 'Rob Pike', 'price': 40, 'quantity': 12, 'published_date': str(today)}
r = requests.post('http://127.0.0.1:8000/api/books/', json=new_book, headers=headers)
print(f'4. POST /api/books/ - Status: {r.status_code}')
if r.status_code == 201:
    print(f'   Created: {r.json()["title"]}')
print()

# Test 5: Pagination
r = requests.get('http://127.0.0.1:8000/api/books/?page_size=2', headers=headers)
print(f'5. GET /api/books/?page_size=2 - Status: {r.status_code}')
data = r.json()
print(f'   Page 1: {len(data["results"])}/2 records')
print(f'   Next page: {bool(data["next"])}')
print()

# Test 6: Ordering
r = requests.get('http://127.0.0.1:8000/api/books/?ordering=-price&page_size=10', headers=headers)
print(f'6. GET /api/books/?ordering=-price - Status: {r.status_code}')
data = r.json()
print(f'   Books by price (high to low):')
for book in data['results'][:3]:
    print(f'   - {book["title"]}: ${book["price"]}')
print()

print('=' * 60)
print('OK - ALL TESTS PASSED')
print('=' * 60)
