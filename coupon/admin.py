from django.contrib import admin
from .models import CouponCode
# Register your models here.
@admin.register(CouponCode)

class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'is_active')
    list_editable = ('discount', 'is_active')
    search_fields = ('code',)
    list_filter = ('valid_from', 'valid_to', 'is_active')