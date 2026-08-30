from rest_framework import serializers
from author.models import Author
from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'count']


class AuthorSerializer(serializers.ModelSerializer):

    books = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Book.objects.all(), 
        required=False
    )

    class Meta:
        model = Author
        fields = ['id', 'name', 'surname', 'patronymic', 'books']

    def create(self, validated_data):
        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        if books_data:
            author.books.add(*books_data)
        return author


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['books'] = BookSerializer(instance.books.all(), many=True).data
        return representation
