from django.db import models
from .search import ProductIndex
from utils.mixins import AuditModelMixin, EnableStatusModelMixin, CityModelMixin
from utils.coremodels import BaseTimestampedModel


class CategoryModel(BaseTimestampedModel):
    """
    Model which defines the categories
    """
    name = models.CharField(
        verbose_name='Category Name', max_length=255, unique=True, db_index=True)

    class Meta:
        """
        Meta data for Category model
        """
        db_table = 'ra_category'

    def __str__(self) -> str:
        return self.name


class Product(EnableStatusModelMixin, AuditModelMixin, CityModelMixin):
    """
    Model which will store details about a product
    """
    title = models.CharField(verbose_name='Product Name', max_length=255)
    description = models.TextField()
    prd_rating = models.DecimalField(
        verbose_name="Product Rating", decimal_places=1, max_digits=2, default=0.0)
    category = models.ForeignKey(
        'core.CategoryModel', on_delete=models.CASCADE)
    small_img = models.ImageField(
        upload_to="products", verbose_name="Product Thumbnail Image", blank=True, null=True)
    rent_daily = models.DecimalField(
        verbose_name="Daily Rent Amount", decimal_places=2, max_digits=100, default=0.00)
    rent_weekly = models.DecimalField(
        verbose_name="Weekly Rent Amount", decimal_places=2, max_digits=100, default=0.00)
    rent_monthly = models.DecimalField(
        verbose_name="Monthly Rent Amount", decimal_places=2, max_digits=100, default=0.00)
    min_rent_days = models.IntegerField(
        verbose_name="Minimum Days To Rent", default=1)
    max_rent_days = models.IntegerField(
        verbose_name="Maximum Days To Rent", default=1)
    security_deposit = models.DecimalField(
        verbose_name="Security Deposit Amount", decimal_places=2, max_digits=100, default=0.00)
    street = models.CharField(
        verbose_name='Street Name', max_length=255, blank=True, null=True)
    location = models.CharField(
        verbose_name='Location', max_length=255, blank=True, null=True)
    tags = models.TextField(default="")

    def indexing(self):
        obj = ProductIndex(
            meta={'id': self.id},
            title=self.title,
            description=self.description,
            category=self.category.name,
            small_img=self.small_img.url if self.small_img else None,
            rent_daily=self.rent_daily,
            city=self.get_city_display(),
            street=self.street,
            location=self.location,
            created_at=self.created_at,
            enable_status=self.enable_status
        )
        taglist = self.tags.split(",")
        if taglist:
            for i in taglist:
                obj.tags.append(i.strip())
        obj.save()
        return obj.to_dict(include_meta=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        """
        Meta data for Product model
        """
        db_table = 'ra_product'


class Review(BaseTimestampedModel):
    """
    Model which will store product reviews
    """
    prd_id = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    headline = models.CharField(verbose_name='Headline', max_length=255)
    description = models.TextField()
    rating = models.DecimalField(
        verbose_name="Product Rating", decimal_places=1, max_digits=2, default=0.0)
    review_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        """
        Meta data for Review Model
        """
        db_table = 'ra_product_review'
