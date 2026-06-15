import django_filters
from rest_framework import filters
from book.models import Book

class BookCustomFilter(django_filters.FilterSet):
    """
    Custom Filter cho Book model
    Cho phép filter theo: title, author, price, quantity
    """
    # Filter theo title (chứa)
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Tìm kiếm theo tên sách (chứa)'
    )
    
    # Filter theo author (chứa)
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains',
        label='Tìm kiếm theo tác giả (chứa)'
    )
    
    # Filter theo price (từ giá tối thiểu đến tối đa)
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Giá tối thiểu'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Giá tối đa'
    )
    price = django_filters.RangeFilter(
        field_name='price',
        label='Khoảng giá'
    )
    
    # Filter theo quantity (từ số lượng tối thiểu đến tối đa)
    quantity_min = django_filters.NumberFilter(
        field_name='quantity',
        lookup_expr='gte',
        label='Số lượng tối thiểu'
    )
    quantity_max = django_filters.NumberFilter(
        field_name='quantity',
        lookup_expr='lte',
        label='Số lượng tối đa'
    )
    quantity = django_filters.RangeFilter(
        field_name='quantity',
        label='Khoảng số lượng'
    )
    
    # Filter theo published_date (từ ngày đến ngày)
    published_date_after = django_filters.DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Xuất bản từ ngày'
    )
    published_date_before = django_filters.DateFilter(
        field_name='published_date',
        lookup_expr='lte',
        label='Xuất bản đến ngày'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'price_min', 'price_max', 'quantity_min', 'quantity_max']


class CustomBookFilter(filters.BaseFilterBackend):
    """
    Custom Filter Backend cho Book ViewSet
    Xử lý filter logic tùy chỉnh
    """
    
    def filter_queryset(self, request, queryset, view):
        """
        Filter queryset dựa trên query parameters
        """
        # Lấy query parameters
        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)
        price_min = request.query_params.get('price_min', None)
        price_max = request.query_params.get('price_max', None)
        quantity_min = request.query_params.get('quantity_min', None)
        quantity_max = request.query_params.get('quantity_max', None)
        
        # Filter theo title (icontains - không phân biệt hoa/thường)
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        # Filter theo author (icontains - không phân biệt hoa/thường)
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        # Filter theo price range
        if price_min:
            try:
                queryset = queryset.filter(price__gte=float(price_min))
            except (ValueError, TypeError):
                pass
        
        if price_max:
            try:
                queryset = queryset.filter(price__lte=float(price_max))
            except (ValueError, TypeError):
                pass
        
        # Filter theo quantity range
        if quantity_min:
            try:
                queryset = queryset.filter(quantity__gte=int(quantity_min))
            except (ValueError, TypeError):
                pass
        
        if quantity_max:
            try:
                queryset = queryset.filter(quantity__lte=int(quantity_max))
            except (ValueError, TypeError):
                pass
        
        return queryset
