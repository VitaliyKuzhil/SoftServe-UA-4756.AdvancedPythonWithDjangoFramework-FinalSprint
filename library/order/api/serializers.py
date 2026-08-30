from rest_framework import serializers
from authentication.forms import CustomUser
from book.models import Book
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'book', 'user', 'copies', 'created_at', 'end_at', 'plated_end_at', 'is_active']

        read_only_fields = ['id', 'created_at']


    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())


    def create(self, validated_data):
        order = Order.create(
            user=validated_data['user'],
            book=validated_data['book'],
            plated_end_at=validated_data['plated_end_at']
        )
        
        if order is None:
            raise serializers.ValidationError({"error": "The book hasn't available yet."})
            
        return order


    def update(self, instance, validated_data):
            update_kwargs = {
                'plated_end_at': validated_data.get('plated_end_at', instance.plated_end_at),
                'end_at': validated_data.get('end_at', instance.end_at),
            }

            instance.update(**update_kwargs)

            if 'user' in validated_data:
                instance.user = validated_data['user']
            if 'book' in validated_data:
                instance.book = validated_data['book']

            if 'is_active' in validated_data:
                instance.is_active = validated_data['is_active']

            if 'copies' in validated_data:
                instance.copies = validated_data['copies']

            instance.save()

            return instance
