from django.contrib import admin
from .models import Category, Product, ProductImage

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProfuctAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'updated')
    list_editable = ('price', 'available')
    list_filter = ('price', 'available', 'created', 'updated')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImegeAdmin(admin.ModelAdmin):
    list_display = ('product',)
