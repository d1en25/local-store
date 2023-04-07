from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from users.models import User
from products.models import Product, ProductCategory, Basket
from common.views import *


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = "Store"


class ProductsListView(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context["title"] = "Store-Каталог"
        context["categories"] = ProductCategory.objects.all()
        return context


# def products(request, category_id=None):
# products = (
#     Product.objects.filter(category_id=category_id)
#     if category_id
#     else Product.objects.all()
# )
# per_page = 3
# paginator = Paginator(products, per_page)
# page_number = request.GET.get("page")
# page_obj = paginator.get_page(page_number)

# categories = ProductCategory.objects.all()
# context = {
#     "title": "Store-Каталог",
#     "categories": categories,
#     "page_obj" : page_obj,
# }
# return render(request, "products/products.html", context)


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
