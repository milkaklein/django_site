
from django.contrib import admin

#from Product import Product
from .models import Products,ProductBySupplier,Suppliers,product_in_zap

admin.site.register(Products)
admin.site.register(ProductBySupplier)
admin.site.register(Suppliers)
admin.site.register(product_in_zap)









