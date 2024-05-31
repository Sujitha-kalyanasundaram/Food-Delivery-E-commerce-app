from django.contrib import admin
from foodapp.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','is_active']
    list_filter=['cat','price','is_active']
    
admin.site.register(Product,ProductAdmin)