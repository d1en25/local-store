from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    def test_index(self):
        path = reverse("index")
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/index.html")
        self.assertEqual(response.context_data["title"], "Store")


class ProductsListViewTestCase(TestCase):
    fixtures = ["product.json", "product_category.json"]

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse("products:products")
        respone = self.client.get(path)

        self._common_tests(respone)
        self.assertEqual(
            list(respone.context_data["object_list"]), list(self.products[:3])
        )

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse("products:category", kwargs={"category_id": category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data["object_list"]),
            list(self.products.filter(category_id=category.id)),
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertEqual(response.context_data["title"], "Store-Каталог")
