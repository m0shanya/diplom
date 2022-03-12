from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_add(request, product_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            cart = Cart(request)
            product = Product.objects.get(id=product_id)
            form = CartAddProductForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                cart.add(product=product,
                         quantity=cd['quantity'],
                         update_quantity=cd['update'])
            return redirect('cart')
    else:
        return redirect('/login/', )


def cart_remove(request, product_id):
    if request.user.is_authenticated:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart')
    else:
        return redirect('/login/', )


def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        return render(request, 'cart/detail.html', {'cart': cart})
    else:
        return redirect('/login/', )
