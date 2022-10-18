from django.contrib import admin
from .models import CategoryModel, Product

# Register your models here.

admin.site.register(CategoryModel)
admin.site.register(Product)
