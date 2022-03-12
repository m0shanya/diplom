import logging

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from shop.forms import LoginForm
from shop.models import Product, Buy
from cart.forms import CartAddProductForm

logger = logging.getLogger(__name__)


def prod_list(request):
    prod = Product.objects.all()
    return render(request, "shop/list.html", {"products": prod})


def product_details_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_cart_form = CartAddProductForm()
    if request.method == "POST":
        if request.POST.get("count"):
            Buy.objects.create(purchase=product, user=request.user, count=request.POST.get("count"))
            return redirect("product_details_view", product_id=product_id)
    return render(request, "shop/details.html", {"product": product, 'product_cart_form': product_cart_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(request, f"Authenticated successfully")
                    return redirect('/', )
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/', )
    return render(request, "shop/logout.html", )
