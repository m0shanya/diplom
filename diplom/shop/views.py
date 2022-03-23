import logging

from django.shortcuts import redirect, render, get_object_or_404

from shop.models import Product, Buy, Category
from cart.forms import CartAddProductForm

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
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("count"):
                Buy.objects.create(purchase=product, user=request.user, count=request.POST.get("count"))
                return redirect("product_details_view", product_id=product_id)
        else:
            return redirect('/login/', )
    return render(request, "shop/details.html", {"product": product, 'product_cart_form': product_cart_form})

