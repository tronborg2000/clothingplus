from django.urls import path
from . import views

urlpatterns = [
    path('account/create/', views.RegisterView.as_view(), name='signup'),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),

]
