import sys
import re
import django

from django.db import transaction

from variables import *
from query import *
#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#

def clear_list():
    del prov_num_fact_var[:]
    del doc_num_fact_var[:]
    del doc_date_fact_var[:]
    del doc_date_exp_fact_var[:]
    del control_accoun_var[:]
    del currency_fact_var[:]
    del doc_num_item_fact_var[:]
    del desc_item_fact_var[:]
    del item_num_fact_var[:]
    del article_fact_var[:]
    del amount_fact_var[:]
    del amount_item_fact_var[:]
    del norm_fact_var[:]
    del memo_fact_var[:]
    del tax_type_fact_var[:]
    del currency_item_fact_var[:]
    del quantity_fact_var[:]
    del wHouse_fact_var[:]
    del date_from_fact_var[:]
    del date_until_fact_var[:]
    del norm_f_fact_var[:]
    del free_text_fact_var[:]

#--------------------------------------------------------------#


def create_prov(rut,name):
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

def create_doc_fact(rut_prov,doc_num,doc_type,date_issue,total,iva,currency_type,iva_min,date_exp, cod_doc, sobre):
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

def create_item_fact_17453(doc_number, line_number, item_name_ret, quantity, amount_ret, iva_type, cod, desc):
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

def create_item(rut, doc_number, line_number, item_name, quantity, amount, iva_type_item, cod, desc, amount_item, amount_iva):       
    try:
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

    print(doc_number, line_number, item_name,quantity,amount, 'Item guardado')

#--------------------------------------------------------------------------------------#

def add_data_fact(desde,hasta,cuenta, doc_number,consumo, lectura_act, lectura_ant):
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


def get_doc_fact(doc_num, prov_num, date, date_exp, currency, control_account, amount, memo):  
    try:
        doc_num_fact_var.append(doc_num)
        prov_num_fact_var.append(prov_num)
        doc_date_fact_var.append(date.strftime('%Y%m%d'))
        doc_date_exp_fact_var.append(date_exp.strftime('%Y%m%d'))
        currency_fact_var.append(currency)
        control_accoun_var.append(control_account)
        amount_fact_var.append('')
        memo_fact_var.append(memo)
    except Exception as e:
        print(f'Error al agregar datos del Documento (Fun getDocFact) - {str(e)}')


def get_item_fact(doc_num, item_line, art, item_amount, norm_g, norm_f, currency, tax, quantity, whouse, date_from, date_until, desc,free_text ):
    try:
        doc_num_item_fact_var.append(doc_num)
        item_num_fact_var.append(item_line)
        article_fact_var.append(art)
        amount_item_fact_var.append(item_amount)
        norm_fact_var.append(norm_g)
        norm_f_fact_var.append(norm_f)
        currency_item_fact_var.append(currency)
        tax_type_fact_var.append(tax)
        quantity_fact_var.append(quantity)
        wHouse_fact_var.append(whouse)
        date_from_fact_var.append(date_from.strftime('%Y%m%d'))
        date_until_fact_var.append(date_until.strftime('%Y%m%d'))
        desc_item_fact_var.append(desc)
        free_text_fact_var.append(free_text)
    except Exception as e:
        print(f'Error al agregar datos del Item (Fun getItemFact) - {str(e)}')


def get_iva_type(item):
    try:
        if item.iva_type in tax_map:
            tax = tax_map[item.iva_type]
    except Exception as e:
        print(f'Error al obtener tipo de Iva (Fun getIvaType) - {str(e)}')
        tax = 'NULL'
    return tax


def get_art(item, name):
    try:
        if name == 'UTE':
            if item.iva_type == "0":
                art = 'GTO000054'
            else:
                art_ute = Article.objects.get(name__icontains='UTE')
                art = art_ute.cod_sap

    except Exception as e:
        print(f'Error al obtener el Articulo (Fun getArt) - {str(e)} - Prov: {item.doc_number.rut} - Item: {item.item_name} - Doc: {item.doc_number.doc_number}' )

    return art

#--------------------------------------------------------------------------------------#

def get_norm_finan(item):
    if item.doc_number.rut.rut in (80073770017, 215166390012, 213108740018, 218878260019, 214111700011):
        cod = AdData.objects.get(doc_number = item.doc_number).account
        norm_g = norma_financieras.get(cod, 'NULL')
        return norm_g

    else:    
        try:
            norm_g = item.doc_number.rut.norma.cod_sap
        except:
            norm_g = 'NULL'
        return norm_g

def get_norm_ute(add_data, account):
    try:
        cod_norm = 'Null'
        norm_g = cod_norm.norm
        norm_f = 'F_212'
        whouse = cod_norm.num_suc
    except:
        if account == '0655141000':
            norm_g = 'G_26'
            norm_f = 'F_212'
            whouse = '026'
        elif account in ['1813951000', '4140591000']:
            norm_g = 'G_69'
            norm_f = 'F_212'
            whouse = '069'
        else:
            norm_g = 'NULL'
            norm_f = 'F_212'
            whouse = 'NULL'
    return norm_g, norm_f, whouse

#--------------------------------------------------------------------------------------#

def get_item_amount_finan(fact, item, tax_finan):
    if fact.rut.name in ('Credisur','Marcre') and tax_finan == 'IVA CTB':
        item_amount = item.sub_amount /1.22
    else:
        item_amount = item.sub_amount
    return item_amount

def get_item_amount_ute(item, add_data):
    try:
        imp_unit = round(float(item.sub_amount),2)
    except:
        imp_unit = item.sub_amount
    return imp_unit

def get_item_amount(item):
    try:
        if item.sub_amount != 0 and item.iva_type == '0':
            amount_item = round(float(item.sub_amount) / float(item.quantity),2)

        elif item.sub_amount != 0 and item.iva_type == '10':
            amount_item = round(float(item.sub_amount) / float(item.quantity),2)
            amount_item = amount_item / 1.10

        elif item.sub_amount != 0 and item.iva_type == '22':
            amount_item = round(float(item.sub_amount) / float(item.quantity),2)
            amount_item = amount_item / 1.22

        else:
            amount_item = 0
            
    except Exception as e:
        print(f'Ha ocurrido un error al calcular el importe del item - {str(e)}')

    return amount_item

#--------------------------------------------------------------------------------------#

def get_cant_unit_ute(item, add_data):
    try:
        cant_unit = add_data.cons_lect
    except:
        cant_unit = item.quantity
    return cant_unit

#--------------------------------------------------------------------------------------#

def get_item_finan(item, art_id):
    try:
        if item.item_name == retencion:
            art = ret_cod

        elif item.doc_number.rut.rut == 80073770017:
            cod = AdData.objects.get(doc_number = item.doc_number).account
            articles = {
                '3239 - cupones':'GTO000043',
                '3239 - ordenes':'GTO000030',
                '31207 - cupones':'GTO000043',
                '64400 - cupones':'GTO000043',
            }
            art = articles.get(cod, 'NULL')

        elif item.item_name == cost_envio:
            art = cost_cod
        elif item.item_name == financiacion:
            art = finan_cod
        elif item.doc_number.rut.rut == 214111700011:
            cod = item.item_name
            articles = {
                'Comisiones por servicios':'GTO000634',
                'Cargos por ventas':'GTO000634',
                'Bonificaciones por servicios':'GTO000634',
                'Finance OFF':'GTO000634',
                'Cargos / bonificaciones por envíos':'GTO000811',
            }
            art = articles.get(cod, 'NULL')            

        elif item.doc_number.rut.rut == 218878260019:
            cod = item.item_name
            articles = {
                'Comisiones por servicios':'GTO000634',
                'Cargos por ventas':'GTO000634',
                'Bonificaciones por servicios':'GTO000634',
                'Finance OFF':'GTO000634',
                'Cargos / bonificaciones por envíos':'GTO000811',
            }
            art = articles.get(cod, 'NULL')            
        else:
            art = art_id.cod_sap
    except Exception as e:
        print(str(e))
    return art



def getAccountFinan(item,resg):
    if item.doc_number.rut.rut == 215166390012:
        cod = AdData.objects.get(doc_number = item.doc_number).account
        accounts = {
            '11020401':'101118',
            '11020413':'101135',
            '13338501':'101118',
            '13338503':'101135',
            '13881101':'101135',
        }
        account = accounts.get(cod, 'NULL')
        return account

    else:    
        try:
            account = resg.rut.cta_sap
        except:
            account = 'NULL'
        return account