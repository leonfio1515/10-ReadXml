from variables import *
import sys
import django
from django.db import transaction
from query import *
#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#


def CreateProv(rut,name):
    try:
        with transaction.atomic():
            ProvType.objects.create(
                rut = rut,
                name = name,
                prov_sap = 'N/A',
                cta_sap = '999',
                prov_type = 'Undefined',
            )
        return print(f'Prov creado - {rut} - Name: {name}\n')

    except Exception as e:
        print (f'Error al crear el proveedor - rut {rut} (Fun CreateProv) - {str(e)} {name}\n')

#--------------------------------------------------------------------------------------#

def CreateDocFact(rut_prov,doc_num,doc_type,date_issue,total,iva,currency_type,iva_min,date_exp, cod_doc, sobre):
    try:
        DocXml.objects.create(
            rut = rut_prov,
            doc_number = doc_num,
            doc_type = doc_type,
            date_issue = date_issue,
            date_exp = date_exp,
            total = total,
            iva_basic = iva,
            iva_min = iva_min,
            currency = currency_type,
            cod_doc = cod_doc,
            sobre = sobre,
        )
    except Exception as e:
        print(f'Error al crear el documento (Fun CreateDocFact) - {str(e)}')

    return print(rut_prov, rut_prov.name, doc_num, doc_type, date_issue, total, iva, sobre, 'Documento guardado')

#--------------------------------------------------------------------------------------#

def CreateItemFact17453(doc_number, line_number, item_name_ret, quantity, amount_ret, iva_type, cod, desc):
    try:
        Item.objects.create(
            doc_number = doc_number,
            line_number = 2,
            item_name = item_name_ret,
            quantity = 1,
            amount_total = float(amount_ret),
            iva_type = 0,
            iva_amount = 0,
            sub_amount = float(amount_ret),
            desc_porc = desc,
            cod = cod,
        )
    except Exception as e:
        print(f'Error al crear item de Factura 17453 - (Fun CreateItemFact17453) - {doc_number} - {str(e)}')

    return print(doc_number, item_name_ret,amount_ret, 'Item guardado')

#--------------------------------------------------------------------------------------#

def CreateItem(rut, doc_number, line_number, item_name, quantity, amount, iva_type, cod, desc):       
    try:
        if int(iva_type) == 1:
            iva_type_item = 0
        elif int(iva_type) == 2:
            iva_type_item = 10
        elif int(iva_type) == 3:
            iva_type_item = 22
        else:
            iva_type_item = 0

        if int(iva_type) == 7 and item_name in redondeos:
            amount_item = float(amount) *-1
            amount_iva = float(amount) * iva_type_item /100
        elif rut == '211223510015':
            amount_iva = float(amount) - (float(amount) / ((iva_type_item /100)+1))
            amount_item = float(amount) - amount_iva
        else:
            amount_item = float(amount)
            amount_iva = float(amount) * iva_type_item /100



        Item.objects.create(
            doc_number = doc_number,
            line_number = line_number,
            item_name = item_name,
            quantity = float(quantity),
            amount_total = amount_item + amount_iva,
            iva_type = iva_type_item,
            iva_amount = amount_iva,
            sub_amount = amount_item,
            desc_porc = desc,
            cod = cod,
        )
    except Exception as e:
        print(f'Error al crear Item de factura (Fun CreateItem) - {doc_number} - {str(e)}')

    print(doc_number, line_number, item_name,quantity,amount, 'Item guardado', int(iva_type))

#--------------------------------------------------------------------------------------#

def AdDataFact(desde,hasta,cuenta, doc_number,consumo, lectura_act, lectura_ant):
    try:
        with transaction.atomic():
            AdData.objects.create(
                doc_number = doc_number,
                date_from = desde,
                date_until = hasta,
                account = cuenta,
                lect_ant = lectura_ant,
                lect_act = lectura_act,
                cons_lect = consumo,

            )
            return print(doc_number,desde, hasta, cuenta,'Aditional data save')
        
    except Exception as e:
        print(f'{str(e)} - No aditional data - {doc_number}')
#--------------------------------------------------------------------------------------#
