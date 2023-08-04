from rest_framework import serializers

from accounts.serializers import GetFullUserSerializer
from products.models import ProductCategory, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'category_slug']


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    category = serializers.SlugRelatedField(slug_field='category_slug', queryset=ProductCategory.objects.all())
    product_name_slug = serializers.SerializerMethodField()
    product_owner = GetFullUserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = ['id', 'product_owner', 'category',
                  'product_name',
                  'product_name_slug',
                  'price',
                  'description',
                  'features',
                  'location',
                  'total_votes',
                  'image',
                  ]

    def get_product_name_slug(self, obj):
        return obj.product_name_slug
