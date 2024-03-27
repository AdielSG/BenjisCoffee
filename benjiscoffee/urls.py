"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pedidos import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('orders/', views.orders, name='orders'),
    path('products/', views.products, name='products'),
    path('orders_completed/', views.orders_completed, name='orders_completed'),
    path('orders/create/', views.create_order, name='create_orders'),
    path('orders/<int:orders_id>/', views.order_detail, name='order_detail'),
    path('products/<int:products_id>/', views.product_detail, name='product_detail'),
    path('orders/<int:orders_id>/complete', views.complete_order, name='complete_order'),
    path('orders/<int:orders_id>/delete', views.delete_order, name='delete_order'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),

    path('cart/<int:cart_id>/', views.cart, name='cart'),
    path('cart/admin/<int:cart_id>/', views.cart_admin, name='cart_admin'),
    path('cart/client/<int:cart_id>/', views.cart_client, name='cart_client'),
    path('cart/admin/<int:cart_id>/complete/', views.complete_client_order, name='complete_client_order'),
    path('add_to_cart', views.add_to_cart, name='add'),
    path('cart/<int:cart_id>/delete', views.delete_cart, name='delete_cart'),
    path('cart/<int:cart_id>/complete/', views.complete_cart, name='complete_cart'),
    path('orders/me/', views.my_orders, name='orders_me'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
