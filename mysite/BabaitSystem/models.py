#from django.db import models
from django.db.models import Model
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import CASCADE
from django.db.models import ForeignKey
from django.db.models import URLField





class Suppliers(Model):
    supplierNmae = CharField(max_length=20)
    site = URLField(max_length=100)
    phone=CharField(max_length=15)

    def __str__(self):
        return self.supplierNmae

    class Meta:
        verbose_name = 'ספקים'
        verbose_name_plural = 'ספקים'


class Products(Model):
    product = CharField(max_length=100)
    makat = CharField(max_length=20)
    ourPrice = IntegerField(default=0)

    def __str__(self):
        return self.product
    class Meta:
        verbose_name = 'מוצרים'
        verbose_name_plural = 'מוצרים'


class ProductBySupplier(Model):
    #product = ForeignKey(Products, on_delete=CASCADE)
    product = CharField(max_length=100)
    supplier = CharField(max_length=20)
    price = IntegerField(default=0)
    makat = CharField(max_length=50,default="")

    def __str__(self):
        return self.product+" אצל "+self.supplier
    class Meta:
        verbose_name = 'מוצרים לפי ספקים'
        verbose_name_plural = 'מוצרים לפי ספקים'


class product_in_zap(Model):
    product = CharField(max_length=100)
    supplier = CharField(max_length=20)
    price = IntegerField(default=0)
    makat = CharField(max_length=50, default="")

    def __str__(self):
        return self.product
    class Meta:
        verbose_name = 'מוצרים בזאפ'
        verbose_name_plural = 'מוצרים בזאפ'


