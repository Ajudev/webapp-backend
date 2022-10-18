from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, AuthViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserViewSet)
router.register(r'auth', AuthViewSet, 'auth')

urlpatterns = [
    path('', include(router.urls)),
]
