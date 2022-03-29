import logging

from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum, F

from cart.cart import Cart
from shop.models import Product, Category, Order, Comment
from cart.forms import CartAddProductForm
from shop.forms import OrderForm, CommentForm, ProductFiltersForm

logger = logging.getLogger(__name__)


def prod_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    prod = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        prod = prod.filter(category=category)

    filters_form = ProductFiltersForm(request.GET)

    if filters_form.is_valid():
        cost__gt = filters_form.cleaned_data["cost__gt"]
        if cost__gt:
            prod = prod.filter(cost__gt=cost__gt)

        cost__lt = filters_form.cleaned_data["cost__lt"]
        if cost__lt:
            prod = prod.filter(cost__lt=cost__lt)

        order_by = filters_form.cleaned_data["order_by"]
        if order_by:
            if order_by == "cost_asc":
                prod = prod.order_by("cost")
            if order_by == "cost_desc":
                prod = prod.order_by("-cost")
            if order_by == "max_count":
                prod = prod.annotate(total_count=Sum("purchases__count")).order_by(
                    "-total_count"
                )
            if order_by == "max_price":
                prod = prod.annotate(
                    total_cost=Sum("purchases__count") * F("cost")
                ).order_by("-total_cost")

    return render(request, "shop/list.html",
                  {"products": prod, 'category': category, 'categories': categories, "filters_form": filters_form})


def product_details_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_cart_form = CartAddProductForm()
    comments = Comment.objects.filter(product=product, active=True)
    return render(request, "shop/details.html",
                  {"product": product, 'product_cart_form': product_cart_form, 'comments': comments})


def comment_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                logger.info(form.cleaned_data)
                new_comment = Comment.objects.create(
                    product=product,
                    name=form.cleaned_data['name'],
                    email=request.user.email,
                    body=form.cleaned_data['body']
                )
                new_comment.save()
                return redirect(f'/product/{product_id}/')
        else:
            form = CommentForm()
        return render(request,
                      'comments/comment_add.html',
                      {'product': product,
                       'form': form})
    else:
        return redirect('/login/', )


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
                                                postal_code=form.cleaned_data['postal_code'],
                                                delivery=form.cleaned_data['delivery'])
                    ordr.save()
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
