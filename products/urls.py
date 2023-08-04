from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ProductCategoriesListView.as_view(), name='categories'),
    path('create/product/', views.ProductCreateView.as_view(), name='create_product'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/vote/<int:product_id>/', views.ProductVoteView.as_view(), name='product_vote'),
    path('product/search/', views.ProductSearchEngine.as_view(), name='place-search-engine'),


]