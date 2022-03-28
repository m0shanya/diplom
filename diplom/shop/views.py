import logging

from django.shortcuts import redirect, render, get_object_or_404

from cart.cart import Cart
from shop.models import Product, Category, Order, Comment
from cart.forms import CartAddProductForm
from shop.forms import OrderForm, CommentForm

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


def prod_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = Comment.objects.create(
                post=product,
                name=request.user.first_name,
                email=request.user.email
            )
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'shop/details.html',
                 {'product': product,
                  'comments': comments,
                  'comment_form': comment_form})


def order_list(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                order = []
                logger.info(form.cleaned_data)
                for item in cart:
                    ordr = Order.objects.create(purchase=item['product'],
                                                cost=item['cost'],
                                                count=item['quantity'],
                                                user=request.user,
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                email=form.cleaned_data['email'],
                                                address=form.cleaned_data['address'],
                                                postal_code=form.cleaned_data['postal_code'])
                    order.append(ordr)
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
    product = Product.objects.all()
    order = Order.objects.filter(user=request.user)
    return render(request, "shop/history.html", {"order": order, "product": product})
