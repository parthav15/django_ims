from django.contrib import admin
from . import models

admin.site.register(models.Vendor)
admin.site.register(models.Unit)
admin.site.register(models.Product)

class PurchaseAdmin(admin.ModelAdmin):
    search_fields=['product']
    list_display = ['id','product','qty','price','total_amt','vendor','pur_date']
    readonly_fields = ('total_amt',)
    exclude = ('total_amt',)
admin.site.register(models.Purchase, PurchaseAdmin)

class SaleAdmin(admin.ModelAdmin):
    search_fields=['product']
    list_display = ['id','product','qty','price','total_amt','sale_date']
    readonly_fields = ('total_amt',)
    exclude = ('total_amt',)
admin.site.register(models.Sale, SaleAdmin)


class InventoryAdmin(admin.ModelAdmin):
    search_fields=['product__title','product__unit__title']
    list_display = ['product','pur_qty','sale_qty','total_bal_qty','product_unit','pur_date','sale_date']
admin.site.register(models.Inventory, InventoryAdmin)
