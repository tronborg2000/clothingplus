from django.contrib import admin
from .models import Product, Comment, Vote, ProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_slug']

    prepopulated_fields = {'category_slug': ('name',)}


# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
