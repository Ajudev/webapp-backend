from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, CityCodeViewSet, GetProductViewSet, GetReviewsViewSet, ProductViewSet, ReviewViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'getProducts', GetProductViewSet)
router.register(r'city', CityCodeViewSet, 'city')
router.register(r'review', ReviewViewSet),
router.register(r'getReviews', GetReviewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
