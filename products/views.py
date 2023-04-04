from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductCategory, Basket
from users.models import User
from django.core.paginator import Paginator


def index(request):
    context = {"title": "Store"}
    return render(request, "products/index.html", context)


def products(request, category_id=None):
    products = (
        Product.objects.filter(category_id=category_id)
        if category_id
        else Product.objects.all()
    )
    per_page = 3
    paginator = Paginator(products, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = ProductCategory.objects.all()
    context = {
        "title": "Store-Каталог",
        "categories": categories,
        "page_obj" : page_obj,
    }
    return render(request, "products/products.html", context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return redirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META["HTTP_REFERER"])
