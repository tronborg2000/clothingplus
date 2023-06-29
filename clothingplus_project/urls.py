from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from products.views import (
    product_list,
    product_detail,
    product_create,
    upvote_product,
    product_search,
)
from products.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<int:pk>/upvote/', upvote_product, name='upvote_product'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', product_search, name='product_search'),
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
]
