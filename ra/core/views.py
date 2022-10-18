from customviewset import CustomModelViewSet
from utils.mixins import ExceptionMixin, CustomResponseMixin

from .models import CategoryModel, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes
from .search import run_search
from rest_framework.viewsets import GenericViewSet


# API ViewSets

class CategoryViewSet(CustomModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    remove_field_list = []
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        return super().create(request, message="Category has been created", *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, message="Category has been deleted", *args, **kwargs)


class ProductViewSet(CustomModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    remove_field_list = []
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        # request.data['created_by'] = request.user.id
        mod_data = request.data.copy()
        mod_data['created_by'] = request.user.id
        return super().create(request, message="Product has been created", mod_data=mod_data, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        mod_data = request.data.copy()
        mod_data['updated_by'] = request.user.id
        return super().update(request, message="Product details have been updated", mod_data=mod_data, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, message="Product has been deleted", *args, **kwargs)


class GetProductViewSet(CustomModelViewSet):
    """
    ViewSet which will only deal with fetching products
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    remove_field_list = []
    http_method_names = ['get']

    @action(methods=['GET', ], detail=False)
    def search(self, request):
        param = request.GET['param']
        page_number = request.GET['page']
        return self.custom_response(data=run_search(search_index="product-index", search_term=param), page_number=page_number)


class CityCodeViewSet(CustomResponseMixin, ExceptionMixin, GenericViewSet):
    """
    Viewset which will display the list of cities available with codes for each city
    """
    @action(methods=['GET', ], detail=False)
    def codes(self, request):
        choice = Product.city.field.choices
        choice_data = []
        for i in choice:
            temp_choice = {}
            temp_choice['key'] = i[0]
            temp_choice['name'] = i[1]
            choice_data.append(temp_choice)

        return self.custom_response(data=choice_data)


class ReviewViewSet(CustomModelViewSet):
    """
    ViewSet which will manage reviews for products
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    remove_field_list = []
    http_method_names = ['post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        mod_data = request.data.copy()
        mod_data['review_by'] = request.user.id
        return super().create(request, message="Review has been saved", mod_data=mod_data, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, message="Review has been updated", *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, message="Review has been deleted", *args, **kwargs)


class GetReviewsViewSet(CustomModelViewSet):
    """
    ViewSet which will manage reviews for products
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    remove_field_list = []
    http_method_names = ['get']
