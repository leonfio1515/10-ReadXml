from django.db import models

from .choices import *

#----------------------------------------------------------------#

class ProvType(models.Model):
    rut = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=150)
    prov_sap = models.CharField(max_length=10)
    cta_sap = models.PositiveIntegerField(blank=True,null=True)
    prov_type = models.CharField(max_length=50, choices=type_prov)

    def __str__(self):
        return self.name

class Article(models.Model):
    cod_sap = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class DocXml(models.Model):
    date_create = models.DateField(auto_now_add=True, null=True, blank=True)

    rut = models.ForeignKey(ProvType, on_delete=models.CASCADE)
    doc_number = models.PositiveIntegerField(unique=True)
    doc_type = models.PositiveSmallIntegerField()
    date_exp = models.DateField()
    date_issue = models.DateField()
    total = models.FloatField()
    iva = models.FloatField()   


class Item(models.Model):
    doc_number= models.ForeignKey(DocXml, on_delete=models.CASCADE)
    line_number = models.SmallIntegerField(default=1)
    item_name = models.CharField(max_length=150)
    quantity = models.SmallIntegerField(default=1)
    amount = models.FloatField()
    iva_type = models.CharField(max_length=10, default=22)
    iva_ammount = models.FloatField(default=0)

class AdData(models.Model):
    doc_number = models.ForeignKey(DocXml, on_delete=models.CASCADE, blank=True, null=True)
    date_from = models.CharField(max_length=20, blank=True, null=True)
    date_until = models.CharField(max_length=20, blank=True, null=True)
    account = models.CharField(max_length=50, blank=True, null=True)
    