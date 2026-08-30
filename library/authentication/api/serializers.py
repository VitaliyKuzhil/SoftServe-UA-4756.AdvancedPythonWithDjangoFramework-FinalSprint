from rest_framework import serializers
from authentication.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'middle_name', 
                  'role', 'is_staff', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True} 
        }


    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance
