import json
from datetime import datetime, date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from book.models import Book
from book.serializers import BookListSerializer
from book.validate.validate_create_book import validate_create_book


# Create your views here.

def get_request_data(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None
    return request.POST.dict()


def parse_published_date(value):
    if not value:
        return None

    if isinstance(value, date):
        return value

    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


@csrf_exempt
def books(request):
    data = get_request_data(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    if request.method == "GET":
        book_id = request.GET.get("id")
        if book_id:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return JsonResponse({"error": "Book not found"}, status=404)
            return JsonResponse({"book": BookListSerializer(book).data})

        queryset = Book.objects.all()
        data_books = BookListSerializer(queryset, many=True)
        return JsonResponse({"books": data_books.data})

    if request.method == "POST":
        errors = validate_create_book(data)
    if errors:
        return JsonResponse(errors, status=400)

    title = data.get("title")
    author = data.get("author")
    price = data.get("price")
    quantity = data.get("quantity")

    book = Book.objects.create(
        title=title,
        author=author,
        price=price,
        quantity=quantity,
    )
    return JsonResponse({"message": "Book created successfully"})

@csrf_exempt
def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)
    if request.method == "GET":
        return JsonResponse({"book": BookListSerializer(book).data})
    data = get_request_data(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    if request.method == "PUT":
        errors = validate_create_book(data)
        if errors:
            return JsonResponse(errors, status=400)

        book.title = data.get("title")
        book.author = data.get("author")
        book.price = data.get("price")
        book.quantity = data.get("quantity")
        book.save()
        return JsonResponse({"message": "Book updated successfully"})
    if request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Book deleted successfully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)
    