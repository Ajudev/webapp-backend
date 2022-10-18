from customviewset import CustomModelViewSet
from rest_framework.viewsets import GenericViewSet

from auth.views import CustomObtainAuthToken
from .models import User
from .serializers import UserSerializer
from utils.mixins import ExceptionMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import action
from django.contrib.auth import logout


# API ViewSets

class UserViewSet(CustomModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    remove_field_list = ['password']
    http_method_names = ['get', 'patch', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        return super().create(request, message="User has been created", *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, message="User details has been updated", *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, message="User has been deleted", *args, **kwargs)


class AuthViewSet(ExceptionMixin, CreateModelMixin, GenericViewSet):
    """
    API View for authentication of users which includes registration/login/logout
    """
    serializer_class = UserSerializer

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        data = {
            "status": "Success",
            "message": "User has been created successfully"
        }
        response = self.create(request)
        response.data = data
        return response

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        return CustomObtainAuthToken().as_view()(request=request._request)

    @action(methods=['POST', ], detail=False, permission_classes=[permissions.IsAuthenticated, ])
    def logout(self, request):
        request.user.auth_token.delete()
        logout(request)
        data = {'status': 'Success', 'message': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
