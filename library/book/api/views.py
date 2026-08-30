from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from book.models import Book
from .serializers import BookSerializer


class BookListApiView(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                book = Book.objects.get(pk=id)
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:

                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
            
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'), 
            'count': request.data.get('count')
        }
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            instance = Book.objects.get(pk=id)
        except Book.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            instance.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except:

            return Response({'message': f"Can not delete book {instance.name}"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        try:
            instance = Book.objects.get(pk=id)
        except Book.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id):
        try:
            instance = Book.objects.get(pk=id)
        except Book.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
