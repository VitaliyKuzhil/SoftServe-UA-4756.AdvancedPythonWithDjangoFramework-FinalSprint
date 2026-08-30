from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from author.models import Author
from book.models import Book
from .serializers import AuthorSerializer


class AuthorListApiView(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                author = Author.objects.get(pk=id)
                serializer = AuthorSerializer(author)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except Author.DoesNotExist:

                return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'surname': request.data.get('surname'), 
            'patronymic': request.data.get('patronymic'), 
            'books': request.data.get('books')
        }
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            instance = Author.objects.get(pk=id)
        except Author.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            instance.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except:

            return Response({'message': f"Can not delete author {instance.name}"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        try:
            instance = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id):
        try:
            instance = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
