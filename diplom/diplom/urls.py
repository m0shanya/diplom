"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from cart.views import cart_detail, cart_add, cart_remove
from shop.views import prod_list, user_login, logout_view, product_details_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', prod_list, name='main'),
    path(
        "product/<int:product_id>/", product_details_view, name="product_details_view"
    ),
    path('cart/', cart_detail, name='cart'),
    path('add/<int:product_id>', cart_add, name='cart_add'),
    path('remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
