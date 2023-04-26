from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from users.models import User
from products.models import Product, ProductCategory, Basket
from common.views import *


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = "Store"


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 3
    title = "Store-Каталог"

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        categories = cache.get("categories")
        if not categories:
            context["categories"] = ProductCategory.objects.all()
            cache.set("categories", context["categories"], 30)
        else:
            context["categories"] = categories
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
    Basket.create_or_update(product_id, request.user)
    return redirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META["HTTP_REFERER"])
