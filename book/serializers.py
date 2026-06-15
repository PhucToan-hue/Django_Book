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
