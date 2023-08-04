# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse
# from django.db.models import Q
# from .models import Product
# from .forms import ProductForm
#
#
# def product_list(request):
#     query = request.GET.get('q')
#     category = request.GET.get('category')
#     sort_by = request.GET.get('sort_by')
#
#     products = Product.objects.all()
#
#     if query:
#         products = products.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(category__icontains=query) |
#             Q(location__icontains=query) |
#             Q(features__icontains=query)
#         )
#
#     if category:
#         products = products.filter(category=category)
#
#     if sort_by == 'price':
#         products = products.order_by('price')
#     elif sort_by == 'popularity':
#         products = products.order_by('-votes_total')
#
#     return render(request, 'products/product_list.html', {'products': products})
#
#
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'products/product_detail.html', {'product': product})
#
#
# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'products/product_create.html', {'form': form})
#
#
# def upvote_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     product.upvote()
#     data = {'votes_total': product.votes_total}
#     return JsonResponse(data)
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status
from rest_framework.decorators import permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.models import ProductCategory, Product
from products.serializers import ProductSerializer, CategorySerializer


@permission_classes([AllowAny])
class ProductCategoriesListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer


@permission_classes([AllowAny])
class ProductListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    queryset = Product.objects.all().order_by('-total_votes', 'price')
    serializer_class = ProductSerializer


@permission_classes([IsAuthenticated])
class ProductCreateView(views.APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer

    def post(self, request, format=None):
        error_result = {}
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            category_slug = request.data.get('category')
            category = get_object_or_404(ProductCategory, category_slug=category_slug)
            new_product = serializer.save(product_owner=self.request.user, category=category)
            new_product.save()
            output = "Successfully place uploaded"
            content = {'status': True, 'message': output, 'result': serializer.data,
                       }
            return Response(content, status=status.HTTP_200_OK)
        content = {'status': False, 'message': serializer.errors, 'result': error_result}
        return Response(content, status=status.HTTP_200_OK)


class ProductSearchEngine(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['category__category_slug', 'product_name', 'description', 'features', 'location', 'price']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-total_votes', 'price')
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                category__category_slug__icontains=search_query) | \
                       queryset.filter(product_name__icontains=search_query) | \
                       queryset.filter(description__icontains=search_query) | \
                       queryset.filter(features__icontains=search_query) | \
                       queryset.filter(location__icontains=search_query)
        return queryset


class ProductVoteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        product = get_object_or_404(Product, id=product_id)

        if product.product_owner == request.user:
            resp = {"error": "You Cannot Vote for Your Own Product. "}
            return Response(resp, status=status.HTTP_200_OK)

        else:
            if Product.objects.filter(id=product_id,  users_votes=request.user):
                product.users_votes.remove(request.user)

                resp = {"status": "unvote", "vote": False}
            else:
                product.users_votes.add(request.user)
                resp = {"status": "voted", "vote": True}

            return Response(resp, status=status.HTTP_200_OK)
