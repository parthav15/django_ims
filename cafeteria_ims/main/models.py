from django.db import models

#Vendor
class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="vendor/")
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = '1. Vendors'
    
    def __str__(self):
        return self.full_name
    
#Unit
class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.TextField()
    
    class Meta:
        verbose_name_plural = '2. Units'
    
    def __str__(self):
        return self.title
    
#Product
class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="product/")
    
    class Meta:
        verbose_name_plural = '3. Products'
    
    def __str__(self):
        return self.title

#Purchase
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    qty = models.FloatField()
    price = models.FloatField()
    total_amt = models.FloatField(editable=False)
    pur_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = '4. Purchases'
        
    def save(self,*args,**kwargs):
        self.total_amt = self.qty*self.price
        super(Purchase, self).save(*args, **kwargs)
        
        #Inventory Management Code
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()
        
        if inventory:
            totalBal = inventory.total_bal_qty+self.qty
        else:
            totalBal = self.qty
            
        Inventory.objects.create(
            product=self.product,
            purchase=self,
            sale=None,
            pur_qty=self.qty,
            sale_qty=None,
            total_bal_qty=totalBal
        )
    
#Sale
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()
    price = models.FloatField()
    total_amt = models.FloatField(editable=False)
    sale_date = models.DateTimeField(auto_now_add=True)
    
    customer_name = models.CharField(max_length=50,blank=True)
    customer_mobile = models.CharField(max_length=50)
    customer_address = models.TextField()
    
    class Meta:
        verbose_name_plural = '5. Sales'
        
    def save(self,*args,**kwargs):
        self.total_amt = self.qty*self.price
        super(Sale, self).save(*args, **kwargs)
        
        #Inventory Management Code
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()
        
        if inventory:
            totalBal = inventory.total_bal_qty-self.qty
            
        Inventory.objects.create(
            product=self.product,
            purchase=None,
            sale=self,
            pur_qty=None,
            sale_qty=self.qty,
            total_bal_qty=totalBal
        )
        
#Inventory
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE,default=0,null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE,default=0,null=True)
    pur_qty = models.FloatField(default=0,null=True)
    sale_qty = models.FloatField(default=0,null=True)
    total_bal_qty = models.FloatField()
    
    class Meta:
        verbose_name_plural = '6. Inventory'
        
    def product_unit(self):
        if self.purchase:
            return self.purchase.product.unit.title
        elif self.sale:
            return self.sale.product.unit.title
        return None
        
    def pur_date(self):
        if self.purchase:
            return self.purchase.pur_date
        
    def sale_date(self):
        if self.sale:
            return self.sale.sale_date
