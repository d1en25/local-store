from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, help_text='Enter category')
    description = models.TextField(max_length=256, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'ProductCategories'
        
    def __str__(self):
        return self.name
        
class Product(models.Model):
    name = models.CharField(max_length=256, help_text='Enter name of product')
    description = models.TextField(blank=True, null=True, help_text='Enter description of product')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
    
    