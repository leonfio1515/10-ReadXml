from django.db import models

from .choices import *

#----------------------------------------------------------------#
class Norma(models.Model):
    cod_sap = models.CharField(max_length=10, default='G_100')
    name = models.CharField(max_length=50, blank=True, null=True)
    
class ProvType(models.Model):
    rut = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=150)
    prov_sap = models.CharField(max_length=10)
    cta_sap = models.PositiveIntegerField(blank=True,null=True)
    prov_type = models.CharField(max_length=50, choices=type_prov)
    norma = models.ForeignKey(Norma, on_delete=models.CASCADE, blank=True,null=True)
    control_account = models.CharField(max_length=10, default=1)
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
    iva_min = models.FloatField()   
    iva_basic = models.FloatField()   
    currency = models.CharField(max_length=10, default="UYU")
    cod_doc = models.PositiveSmallIntegerField(blank=True, null=True)  
    sobre = models.CharField(max_length=100, blank=True, null=True)

    id_doc = models.CharField(max_length= 20, unique=True)

    def save(self, *args, **kwargs):
        prov_obj = ProvType.objects.get(rut = self.rut.rut)
        self.id_doc = f'{prov_obj.rut}-{self.doc_number}'
        
        super().save(*args, **kwargs)

class Item(models.Model):
    doc_number= models.ForeignKey(DocXml, on_delete=models.CASCADE)

    line_number = models.SmallIntegerField(default=1)
    item_name = models.CharField(max_length=150)
    quantity = models.SmallIntegerField(default=1)
    amount_total = models.FloatField()
    iva_type = models.CharField(max_length=10, default=1)
    iva_amount = models.FloatField(default=0)
    sub_amount = models.FloatField()
    desc_porc = models.CharField(max_length=10, default=0)
    cod = models.CharField(max_length=100, default='')

class AdData(models.Model):
    doc_number = models.ForeignKey(DocXml, on_delete=models.CASCADE, blank=True, null=True)
    date_from = models.DateField(max_length=20, blank=True, null=True)
    date_until = models.DateField(blank=True, null=True)
    account = models.CharField(max_length=150, blank=True, null=True)
    lect_ant = models.CharField(max_length=20, blank=True, null=True)
    lect_act = models.CharField(max_length=20, blank=True, null=True)    
    cons_lect = models.CharField(max_length=20, blank=True, null=True)  