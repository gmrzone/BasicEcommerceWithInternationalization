from django.db import models
import os
import datetime
from django.utils import timezone
from django.shortcuts import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        url = reverse('home_category', args=[self.slug])
        return url

    def __str__(self):
        return self.name

def image_location(instance, filename):
    time_now = timezone.now()
    loc = os.path.join('product_images', instance.product.slug, time_now.strftime('%Y'), time_now.strftime('%m'), filename)
    return loc


class Product(models.Model):
    name = models.CharField(max_length=300, db_index=True)
    slug = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'))

    def get_absolute_url(self):
        url = reverse('product_detail', args=[self.id, self.slug])
        return url

    def get_single_image(self):
        return self.images.all()[0].image.url

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_location, default='img-default.gif')