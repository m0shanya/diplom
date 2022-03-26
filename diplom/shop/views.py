import logging

from django.shortcuts import redirect, render, get_object_or_404

from cart.cart import Cart
from shop.models import Product, Category, Order, Buy
from cart.forms import CartAddProductForm
from shop.forms import OrderForm

logger = logging.getLogger(__name__)


def prod_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    prod = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        prod = prod.filter(category=category)
    return render(request, "shop/list.html", {"products": prod, 'category': category, 'categories': categories})


def product_details_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_cart_form = CartAddProductForm()
    return render(request, "shop/details.html", {"product": product, 'product_cart_form': product_cart_form})


def order_list(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = OrderForm(request.POST)
            Order.objects.create(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email
            )
            order = Order.objects.get(first_name=request.user.first_name)
            if form.is_valid():
                logger.info(form.cleaned_data)
                for item in cart:
                    Buy.objects.create(order=order,
                                       purchase=item['product'],
                                       cost=item['cost'],
                                       count=item['quantity'])
                cart.clear()
                return render(request, 'shop/order_created.html',
                              {'order': order})
        else:
            form = OrderForm()
    else:
        return redirect('/login/', )
    return render(request, 'shop/order_create.html',
                  {'cart': cart, 'form': form})


def history_list(request):
    order = Buy.objects.all()
    return render(request, "shop/history.html", {"order": order})
