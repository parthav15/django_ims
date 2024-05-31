from django.contrib import admin
from . import models

admin.site.register(models.Vendor)
admin.site.register(models.Unit)

class CustomerAdin(admin.ModelAdmin):
    search_field=['customer_name','customer_mobile']
    list_display=['customer_name','customer_mobile']
admin.site.register(models.Customer)

class ProductAdmin(admin.ModelAdmin):
    search_fields=['title']
    list_display = ['title','unit'] 
admin.site.register(models.Product,ProductAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    search_fields=['product__title']
    list_display = ['vendor','product','qty','price','total_amt','pur_date']
    readonly_fields = ('total_amt',)
    exclude = ('total_amt',)
admin.site.register(models.Purchase, PurchaseAdmin)

class SaleAdmin(admin.ModelAdmin):
    search_fields=['product__title']
    list_display = ['customer','product','qty','price','total_amt','sale_date']
    readonly_fields = ('total_amt',)
    exclude = ('total_amt',)
admin.site.register(models.Sale, SaleAdmin)


class InventoryAdmin(admin.ModelAdmin):
    search_fields=['product__title','product__unit__title']
    list_display = ['product','pur_qty','sale_qty','total_bal_qty','product_unit','pur_date','sale_date','customer_name','vendor_name']
admin.site.register(models.Inventory, InventoryAdmin)
