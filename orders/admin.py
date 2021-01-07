from django.contrib import admin
from .models import Order, OrderItem
import csv
from django.shortcuts import HttpResponse, reverse
from django.http import StreamingHttpResponse
import datetime
from django.utils.safestring import mark_safe

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# # Using Nor Http Respomnse for exporting Csv File
# def export_to_csv(ModelAdmin, request, queryset):
#     opt = ModelAdmin.model._meta
#     content_disposition = f'attachments; filename={opt.verbose_name}.csv'
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = content_disposition
#     writer = csv.writer(response)
#     fields = [field for field in opt.get_fields() if not field.many_to_many and not field.one_to_many]
#     #  Write a first row with header information
#     writer.writerow([field.verbose_name for field in fields])
#     # Write data rows.
#     for object in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(object, field.name)
#             if isinstance(value,datetime.datetime):
#                 data_row.append(value.strftime("%d/%m/%Y"))
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response
# export_to_csv.short_description = "Export to CSV"







# Using SteamingHttpResponse for Exporting Large CSV FIles
class Echo:
    
    def write(self, value):
        return value

def export_to_csv(ModelAdmin, request, queryset):
    opt = ModelAdmin.model._meta
    content_deposition = f'attachments; filename={opt.verbose_name}.csv'
    fields = [field for field in opt.get_fields() if not field.many_to_many and not field.one_to_many]
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    rows = []
    rows.append([field.verbose_name for field in fields])
    for object in queryset:
        current_row = []
        for field in fields:
            value = getattr(object, field.name)
            if isinstance(value, datetime.datetime):
                current_row.append(value.strftime("%d/%m/%y %H-%M-%S"))
            else:
                current_row.append(value)
        rows.append(current_row)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type='text/csv')
    response['Content-Disposition'] = content_deposition
    return response
export_to_csv.short_description = "Export To CSV"

def order_detail(obj):
    url = reverse('admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf_admin(obj):
    url = reverse('get_pdf_admin', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf_admin.short_description = "Invoice"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'address', 'pincode', 'city', 'paid', 'created', 'updated', order_detail, order_pdf_admin)
    list_filter = ('paid', 'pincode', 'city', 'created', 'updated')
    inlines = [OrderItemInline]
    actions = [export_to_csv]