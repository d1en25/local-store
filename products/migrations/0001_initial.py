# Generated by Django 3.2.13 on 2023-04-03 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter category', max_length=128)),
                ('description', models.TextField(blank=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name_plural': 'ProductCategories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter name of product', max_length=256)),
                ('description', models.TextField(blank=True, help_text='Enter description of product', null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(upload_to='products_images')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.productcategory')),
            ],
        ),
    ]