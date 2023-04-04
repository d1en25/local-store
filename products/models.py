from django.db import models
from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, help_text="Enter category")
    description = models.TextField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name_plural = "ProductCategories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, help_text="Enter name of product")
    description = models.TextField(
        blank=True, null=True, help_text="Enter description of product"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products_images")
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()
    def __str__(self):
        return f"Корзина для { self.user.username } | Продукт :{ self.product.name }"

    def sum(self):
        return self.product.price * self.quantity

    def total_sum(self):
        baskets = Basket.objects.get(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.get(user=self.user)
        return sum(basket.quantity for basket in baskets)
