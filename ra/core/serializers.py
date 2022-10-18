from rest_framework.serializers import ModelSerializer, CharField, IntegerField, PrimaryKeyRelatedField

from users.models import User
from .models import CategoryModel, Product, Review


class CategorySerializer(ModelSerializer):
    """
    Model Serializer to validate all input data before storing it to the DB
    """

    class Meta:
        """
        Meta data class
        """
        model = CategoryModel
        fields = ('id', 'name')


class ProductSerializer(ModelSerializer):
    """
    Model Serializer to validate all input data before storing it to the DB
    """

    city = CharField(default="DXB")
    enable_status = CharField(default="ENABLE")
    created_by = PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=None)
    updated_by = PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=None)

    class Meta:
        """
        Meta data class
        """
        model = Product
        fields = ('id', 'title', 'description', 'category', 'small_img', 'rent_daily', 'rent_weekly',
                  'rent_monthly', 'min_rent_days', 'max_rent_days', 'security_deposit', 'street', 'city', 'location', 'created_by', 'updated_by', 'enable_status', 'tags')


class ReviewSerializer(ModelSerializer):
    """
    Model Serializer to validate all input data before storing it to the DB
    """

    class Meta:
        """
        Meta Data Class
        """
        model = Review
        fields = ('id', 'prd_id', 'headline',
                  'description', 'rating', 'review_by')
