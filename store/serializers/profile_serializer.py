from rest_framework import serializers
from django.contrib.auth.models import User
from store.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'phone_number', 'address', 'city', 'state', 'country', 
                 'zip_code', 'profile_picture', 'created_at', 'updated_at', 
                 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        # Update User model fields if provided
        user_data = {}
        if 'email' in validated_data:
            user_data['email'] = validated_data.pop('email')
        if 'first_name' in validated_data:
            user_data['first_name'] = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user_data['last_name'] = validated_data.pop('last_name')
        
        if user_data:
            User.objects.filter(pk=instance.user.pk).update(**user_data)

        # Update Profile model fields
        return super().update(instance, validated_data)
