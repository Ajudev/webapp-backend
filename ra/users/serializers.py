from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Permission
from .models import User


class UserSerializer(ModelSerializer):
    """
    Model Serializer to validate all input data before storing it to the DB
    """

    def create(self, validated_data):
        u_type = validated_data['user_type']
        user = User.objects.create_user(**validated_data)

        if u_type.lower() == "app":
            code_name = 'app_user'
        elif u_type.lower() == "dashboard":
            code_name = 'dashboard_user'

        permission = Permission.objects.get(codename=code_name)
        user.user_permissions.add(permission)

        user.save()
        return user

    class Meta:
        """
        Meta data class
        """
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone',
                  'city', 'gender', 'user_type', 'profile_img')
