from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "is_active", "is_staff"]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True}
        }

    def create(self, validated_data):
        copy_vd = validated_data.copy()
        copy_vd.pop("username")
        copy_vd.pop("password", None)
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            password = validated_data.get('password'),
            **copy_vd
        )
        return user