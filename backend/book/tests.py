from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from book.models import Book


class BookApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="strong-test-password",
        )
        token_response = self.client.post(
            "/api/token/",
            {"username": "tester", "password": "strong-test-password"},
            format="json",
        )
        self.access_token = token_response.data["access"]
        self.refresh_token = token_response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_books_require_authentication(self):
        self.client.credentials()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pagination_supports_page_and_page_size(self):
        Book.objects.bulk_create(
            [
                Book(title=f"Book {index}", author="Author", price=100, quantity=1)
                for index in range(45)
            ]
        )

        response = self.client.get("/api/books/?page=2&page_size=20")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 45)
        self.assertEqual(len(response.data["data"]), 20)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])

    def test_create_update_and_delete_book(self):
        create_response = self.client.post(
            "/api/books/",
            {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "price": 120000,
                "quantity": 5,
                "published_date": "2008-08-01",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        book_id = create_response.data["data"]["id"]

        update_response = self.client.patch(
            f"/api/books/{book_id}/",
            {"quantity": 8},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["data"]["quantity"], 8)

        delete_response = self.client.delete(f"/api/books/{book_id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Book.objects.filter(pk=book_id).exists())

    def test_negative_price_and_quantity_are_rejected(self):
        response = self.client.post(
            "/api/books/",
            {"title": "Invalid", "author": "Author", "price": -1, "quantity": -2},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data["errors"])
        self.assertIn("quantity", response.data["errors"])

    def test_logout_blacklists_refresh_token(self):
        logout_response = self.client.post(
            "/api/logout/",
            {"refresh": self.refresh_token},
            format="json",
        )
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        refresh_response = self.client.post(
            "/api/token/refresh/",
            {"refresh": self.refresh_token},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
