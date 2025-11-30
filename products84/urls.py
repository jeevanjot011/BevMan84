# products84/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('order/<int:product_id>/', views.order_product, name='order_product'),
    path('my-orders/', views.my_orders, name='my_orders'),
]