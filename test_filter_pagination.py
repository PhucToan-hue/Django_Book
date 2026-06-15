import os
import sys
import django
import json
from datetime import datetime, timedelta

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_manage.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from book.models import Book

User = get_user_model()

def setup_test_user():
    """Tạo hoặc lấy user test"""
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    return user

def get_jwt_token(user):
    """Lấy JWT token cho user"""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    return refresh.access_token

def setup_test_data():
    """Tạo dữ liệu test"""
    Book.objects.all().delete()
    
    today = datetime.now().date()
    books = [
        # Python books
        Book.objects.create(title="Python 101", author="Guido van Rossum", price=25, quantity=10, published_date=today),
        Book.objects.create(title="Advanced Python", author="Guido van Rossum", price=45, quantity=5, published_date=today - timedelta(days=10)),
        
        # Django books
        Book.objects.create(title="Django for Beginners", author="William Vincent", price=29, quantity=15, published_date=today - timedelta(days=5)),
        Book.objects.create(title="Django Advanced", author="William Vincent", price=55, quantity=3, published_date=today - timedelta(days=15)),
        
        # FastAPI books
        Book.objects.create(title="FastAPI Modern Web", author="Tiangolo", price=35, quantity=8, published_date=today - timedelta(days=20)),
        
        # JavaScript books
        Book.objects.create(title="JavaScript Beginner", author="Kyle Simpson", price=19, quantity=25, published_date=today - timedelta(days=30)),
        Book.objects.create(title="You Don't Know JS", author="Kyle Simpson", price=39, quantity=7, published_date=today - timedelta(days=25)),
        
        # Database books
        Book.objects.create(title="PostgreSQL Guide", author="Bruce Momjian", price=42, quantity=4, published_date=today - timedelta(days=35)),
        Book.objects.create(title="MySQL Performance", author="Baron Schwartz", price=48, quantity=6, published_date=today - timedelta(days=40)),
        
        # Extra books
        Book.objects.create(title="Golang Basics", author="Rob Pike", price=32, quantity=9, published_date=today - timedelta(days=45)),
    ]
    
    return books

def test_pagination():
    """Test pagination"""
    client = APIClient()
    user = setup_test_user()
    token = get_jwt_token(user)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    print("\n" + "=" * 80)
    print("TEST PAGINATION (Phân Trang)")
    print("=" * 80)
    
    # Test 1: Lấy trang 1 mặc định (20 record/trang)
    print("\n1. LẤY TRANG 1 (Mặc định 20 record/trang)")
    print("-" * 80)
    response = client.get('/api/books/', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total records: {data['count']}")
    print(f"  Records in this page: {len(data['results'])}")
    print(f"  Next page: {data['next']}")
    print(f"  Previous page: {data['previous']}")
    
    # Test 2: Lấy trang 1 với 50 record/trang
    print("\n2. LẤY TRANG 1 VỚI 50 RECORD/TRANG")
    print("-" * 80)
    response = client.get('/api/books/?page_size=50', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Page size: 50")
    print(f"  Records in this page: {len(data['results'])}")
    
    # Test 3: Lấy trang 1 với 100 record/trang (tối đa)
    print("\n3. LẤY TRANG 1 VỚI 100 RECORD/TRANG (TỐI ĐA)")
    print("-" * 80)
    response = client.get('/api/books/?page_size=100', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Page size: 100")
    print(f"  Records in this page: {len(data['results'])}")
    
    # Test 4: Kiểm tra lấy trang 2
    print("\n4. LẤY TRANG 2 (nếu có)")
    print("-" * 80)
    response = client.get('/api/books/?page=2&page_size=5', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    if data['results']:
        print(f"  Trang 2 có dữ liệu:")
        for book in data['results']:
            print(f"    - {book['title']}")
    else:
        print(f"  Không có trang 2 (tổng < page_size)")

def test_filters():
    """Test custom filters"""
    client = APIClient()
    user = setup_test_user()
    token = get_jwt_token(user)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    print("\n" + "=" * 80)
    print("TEST FILTER (Tìm Kiếm)")
    print("=" * 80)
    
    # Test 1: Filter theo title
    print("\n1. FILTER THEO TITLE (title=python)")
    print("-" * 80)
    response = client.get('/api/books/?title=python', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']} ({book['author']})")
    
    # Test 2: Filter theo author
    print("\n2. FILTER THEO AUTHOR (author=guido)")
    print("-" * 80)
    response = client.get('/api/books/?author=guido', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']} ({book['author']})")
    
    # Test 3: Filter theo price_min
    print("\n3. FILTER THEO PRICE_MIN (price_min=40)")
    print("-" * 80)
    response = client.get('/api/books/?price_min=40', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: ${book['price']}")
    
    # Test 4: Filter theo price_max
    print("\n4. FILTER THEO PRICE_MAX (price_max=30)")
    print("-" * 80)
    response = client.get('/api/books/?price_max=30', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: ${book['price']}")
    
    # Test 5: Filter theo price range
    print("\n5. FILTER THEO PRICE RANGE (price_min=30&price_max=45)")
    print("-" * 80)
    response = client.get('/api/books/?price_min=30&price_max=45', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: ${book['price']}")
    
    # Test 6: Filter theo quantity_min
    print("\n6. FILTER THEO QUANTITY_MIN (quantity_min=10)")
    print("-" * 80)
    response = client.get('/api/books/?quantity_min=10', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: {book['quantity']} copies")
    
    # Test 7: Filter theo quantity_max
    print("\n7. FILTER THEO QUANTITY_MAX (quantity_max=5)")
    print("-" * 80)
    response = client.get('/api/books/?quantity_max=5', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: {book['quantity']} copies")

def test_combined():
    """Test kết hợp filter + ordering + pagination"""
    client = APIClient()
    user = setup_test_user()
    token = get_jwt_token(user)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    print("\n" + "=" * 80)
    print("TEST KẾT HỢP (Filter + Ordering + Pagination)")
    print("=" * 80)
    
    # Test 1: title + price + ordering
    print("\n1. KẾT HỢP: title=python & price_max=40 & ordering=-price")
    print("-" * 80)
    response = client.get('/api/books/?title=python&price_max=40&ordering=-price', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: ${book['price']}")
    
    # Test 2: author + quantity + page_size
    print("\n2. KẾT HỢP: author=kyle & quantity_min=5 & page_size=10")
    print("-" * 80)
    response = client.get('/api/books/?author=kyle&quantity_min=5&page_size=10', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']} ({book['quantity']} copies)")
    
    # Test 3: price range + quantity range + ordering
    print("\n3. KẾT HỢP: price_min=30&price_max=50 & quantity_min=3 & ordering=title")
    print("-" * 80)
    response = client.get('/api/books/?price_min=30&price_max=50&quantity_min=3&ordering=title', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {len(data['results'])}")
    for book in data['results']:
        print(f"    - {book['title']}: ${book['price']} ({book['quantity']} copies)")

def test_edge_cases():
    """Test edge cases"""
    client = APIClient()
    user = setup_test_user()
    token = get_jwt_token(user)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    print("\n" + "=" * 80)
    print("TEST EDGE CASES")
    print("=" * 80)
    
    # Test 1: Empty filter result
    print("\n1. FILTER KHÔNG CÓ KẾT QUẢ (title=nonexistent)")
    print("-" * 80)
    response = client.get('/api/books/?title=nonexistent', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Total matched: {data['count']}")
    print(f"  Results: {len(data['results'])}")
    
    # Test 2: Invalid page_size (should clamp to max 100)
    print("\n2. INVALID PAGE_SIZE (page_size=200 -> should be 100)")
    print("-" * 80)
    response = client.get('/api/books/?page_size=200', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Requested: 200, Got: {len(data['results'])} (max 100)")
    
    # Test 3: Invalid price value
    print("\n3. INVALID PRICE VALUE (price_min=abc)")
    print("-" * 80)
    response = client.get('/api/books/?price_min=abc', **headers)
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"  Invalid parameter ignored, total results: {len(data['results'])}")
    
    # Test 4: Case insensitive search
    print("\n4. CASE INSENSITIVE SEARCH (title=PYTHON vs title=python)")
    print("-" * 80)
    response1 = client.get('/api/books/?title=PYTHON', **headers)
    response2 = client.get('/api/books/?title=python', **headers)
    print(f"✓ Status: {response1.status_code}")
    print(f"  PYTHON results: {len(response1.json()['results'])}")
    print(f"  python results: {len(response2.json()['results'])}")
    print(f"  Same results: {len(response1.json()['results']) == len(response2.json()['results'])}")

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("THIẾT LẬP DỮ LIỆU TEST")
    print("=" * 80)
    setup_test_data()
    print("✓ Đã tạo 10 sách test")
    
    test_pagination()
    test_filters()
    test_combined()
    test_edge_cases()
    
    print("\n" + "=" * 80)
    print("KẾT THÚC TEST")
    print("=" * 80)
