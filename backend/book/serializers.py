from rest_framework import serializers
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_title(self, value):
        title = value.strip()
        if not title:
            raise serializers.ValidationError("Tên sách không được để trống.")
        return title

    def validate_author(self, value):
        author = value.strip()
        if not author:
            raise serializers.ValidationError("Tác giả không được để trống.")
        return author

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Giá phải lớn hơn hoặc bằng 0.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Số lượng phải lớn hơn hoặc bằng 0.")
        return value
