import os
import sys
import django
import json

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
        defaults={
            'email': 'test@example.com'
        }
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

def test_api():
    """Test tất cả các endpoint API"""
    client = APIClient()
    
    # Setup
    user = setup_test_user()
    token = get_jwt_token(user)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    print("=" * 60)
    print("TEST API QUẢN LÝ SÁCH")
    print("=" * 60)
    
    # Clear dữ liệu cũ
    Book.objects.all().delete()
    print("\n✓ Đã xóa dữ liệu cũ\n")
    
    # 1. Test POST - Thêm sách mới
    print("1. TEST THÊM SÁCH MỚI (POST /api/books/)")
    print("-" * 60)
    
    test_books = [
        {
            "title": "Python 101",
            "author": "Guido van Rossum",
            "price": 25,
            "quantity": 10,
            "published_date": "2024-01-15"
        },
        {
            "title": "Django for Beginners",
            "author": "William Vincent",
            "price": 29,
            "quantity": 5,
            "published_date": "2024-02-20"
        },
        {
            "title": "FastAPI Modern Web",
            "author": "Tiangolo",
            "price": 35,
            "quantity": 8,
            "published_date": "2024-03-10"
        }
    ]
    
    created_ids = []
    for book_data in test_books:
        response = client.post('/api/books/', book_data, format='json', **headers)
        if response.status_code == 201:
            print(f"✓ Thêm thành công: {book_data['title']}")
            created_ids.append(response.data['id'])
        else:
            print(f"✗ Thêm thất bại: {response.data}")
    
    # 2. Test GET - Lấy danh sách
    print("\n2. TEST LẤY DANH SÁCH SÁCH (GET /api/books/)")
    print("-" * 60)
    response = client.get('/api/books/', **headers)
    if response.status_code == 200:
        print(f"✓ Lấy danh sách thành công")
        print(f"  Tổng sách: {response.data['count']}")
        print(f"  Trang hiện tại: {response.data.get('results', [])}")
    else:
        print(f"✗ Lấy danh sách thất bại: {response.data}")
    
    # 3. Test SEARCH
    print("\n3. TEST TÌM KIẾM (GET /api/books/?search=Python)")
    print("-" * 60)
    response = client.get('/api/books/?search=Python', **headers)
    if response.status_code == 200:
        print(f"✓ Tìm kiếm thành công")
        print(f"  Kết quả: {len(response.data['results'])} sách")
        for book in response.data['results']:
            print(f"    - {book['title']}")
    
    # 4. Test ORDERING
    print("\n4. TEST SẮP XẾP (GET /api/books/?ordering=-price)")
    print("-" * 60)
    response = client.get('/api/books/?ordering=-price', **headers)
    if response.status_code == 200:
        print(f"✓ Sắp xếp theo giá thành công")
        for book in response.data['results']:
            print(f"    - {book['title']}: ${book['price']}")
    
    # 5. Test GET chi tiết
    if created_ids:
        print(f"\n5. TEST LẤY CHI TIẾT SÁCH (GET /api/books/{created_ids[0]}/)")
        print("-" * 60)
        response = client.get(f'/api/books/{created_ids[0]}/', **headers)
        if response.status_code == 200:
            print(f"✓ Lấy chi tiết thành công")
            print(json.dumps(response.data, indent=2, ensure_ascii=False))
        else:
            print(f"✗ Lấy chi tiết thất bại: {response.data}")
        
        # 6. Test PATCH - Cập nhật một phần
        print(f"\n6. TEST CẬP NHẬT MỘT PHẦN (PATCH /api/books/{created_ids[0]}/)")
        print("-" * 60)
        update_data = {
            "price": 45,
            "quantity": 20
        }
        response = client.patch(f'/api/books/{created_ids[0]}/', update_data, format='json', **headers)
        if response.status_code == 200:
            print(f"✓ Cập nhật thành công")
            print(f"  Giá mới: ${response.data['price']}")
            print(f"  Số lượng mới: {response.data['quantity']}")
        else:
            print(f"✗ Cập nhật thất bại: {response.data}")
        
        # 7. Test PUT - Cập nhật toàn bộ
        print(f"\n7. TEST CẬP NHẬT TOÀN BỘ (PUT /api/books/{created_ids[0]}/)")
        print("-" * 60)
        full_update_data = {
            "title": "Python Advanced Topics",
            "author": "Guido van Rossum",
            "price": 50,
            "quantity": 25,
            "published_date": "2024-06-01"
        }
        response = client.put(f'/api/books/{created_ids[0]}/', full_update_data, format='json', **headers)
        if response.status_code == 200:
            print(f"✓ Cập nhật toàn bộ thành công")
            print(json.dumps(response.data, indent=2, ensure_ascii=False))
        else:
            print(f"✗ Cập nhật toàn bộ thất bại: {response.data}")
    
    # 8. Test validation
    print(f"\n8. TEST VALIDATION (POST /api/books/ với dữ liệu không hợp lệ)")
    print("-" * 60)
    invalid_book = {
        "title": "",
        "author": "Test Author",
        "price": "invalid",
        "quantity": 10
    }
    response = client.post('/api/books/', invalid_book, format='json', **headers)
    if response.status_code != 201:
        print(f"✓ Validation hoạt động đúng")
        print(f"  Lỗi: {response.data}")
    else:
        print(f"✗ Validation không hoạt động")
    
    # 9. Test DELETE
    if created_ids:
        print(f"\n9. TEST XÓA SÁCH (DELETE /api/books/{created_ids[-1]}/)")
        print("-" * 60)
        response = client.delete(f'/api/books/{created_ids[-1]}/', **headers)
        if response.status_code == 204:
            print(f"✓ Xóa thành công")
            # Kiểm tra xem sách có còn không
            check_response = client.get(f'/api/books/{created_ids[-1]}/', **headers)
            if check_response.status_code == 404:
                print(f"✓ Sách không còn trong database")
        else:
            print(f"✗ Xóa thất bại: {response.data}")
    
    # 10. Test Statistics
    print(f"\n10. TEST THỐNG KÊ (GET /api/books/statistics/)")
    print("-" * 60)
    response = client.get('/api/books/statistics/', **headers)
    if response.status_code == 200:
        print(f"✓ Lấy thống kê thành công")
        print(json.dumps(response.data, indent=2))
    else:
        print(f"✗ Lấy thống kê thất bại: {response.data}")
    
    print("\n" + "=" * 60)
    print("KẾT THÚC TEST")
    print("=" * 60)

if __name__ == '__main__':
    test_api()
