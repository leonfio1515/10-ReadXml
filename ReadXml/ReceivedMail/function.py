import pandas as pd
from variables import *
import sys
import django
from django.db import transaction
from sendMail import *

#--------------------------------------------------------------------------------------#

#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#


def XlsxFactFinan(data_fact, data_item):
    #--Construye la tabla de Facturas
    df_fact = pd.DataFrame(data_fact)
    subtitulo_fact = ['Correlativo','Cod. Proveedor','DocType','F. Contabilizacion','F. Vencimiento','F. Documento','Nro. Referencia',	'Moneda','Serie','Correlativo','CtlAccount','Series']
    df_fact = pd.concat([pd.DataFrame([subtitulo_fact], columns=df_fact.columns), df_fact], ignore_index=True)


    #--Construye la tabla de Item
    df_item = pd.DataFrame(data_item)
    subtitulo_item = ['Correlativo','Secuencia','Artículo','Saldo del documento (Moneda de documento)','OcrCode','OcrCode2','ESTANDAR','Moneda']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)


    #--Crea el archivo de OPCH
    excel_path_fact = f'{date_download} - Financieras - OPCH Factura1.xlsx'
    df_fact.to_excel(excel_path_fact, index=False)
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{date_download} - Financieras - PCH1 Factura2.xlsx'
    df_item.to_excel(excel_path_item, index=False)
    print(f'Archivo OPCH exportado a {excel_path_item}')

    send_mail_finan_fact(excel_path_item, excel_path_fact, date_download)
#--------------------------------------------------------------------------------------#

def XlsxResg17453Finan(data_resg, resg_item):
    #--Construye la tabla de Facturas
    df_fact = pd.DataFrame(data_resg)
    subtitulo_resg = ['DocNum','DocType','Series','CardCode','DocDate','TaxDate','DocDueDate','Referencia','Ref2','CashSum','CashAccount']
    df_fact = pd.concat([pd.DataFrame([subtitulo_resg], columns=df_fact.columns), df_fact], ignore_index=True)


    #--Construye la tabla de Item
    df_item = pd.DataFrame(resg_item)
    subtitulo_item = ['DocNum','LineNum','AcctCode','SumApplied','Descrip']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)


    #--Crea el archivo de OPCH
    excel_path_fact = f'{date_download} - ORCT pago1 - 17453.xlsx'
    df_fact.to_excel(excel_path_fact, index=False)
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{date_download} - RCT4 Pago2 - 17453.xlsx'
    df_item.to_excel(excel_path_item, index=False)
    print(f'Archivo OPCH exportado a {excel_path_item}')

    send_mail_finan_ret17453(excel_path_item, excel_path_fact, date_download)

#--------------------------------------------------------------------------------------#

def XlsxResg18910Finan(data_resg, resg_item):
    #--Construye la tabla de Facturas
    df_fact = pd.DataFrame(data_resg)
    subtitulo_resg = ['DocNum','DocType','Series','CardCode','DocDate','TaxDate','DocDueDate','Referencia','Ref2','CashSum','CashAccount']
    df_fact = pd.concat([pd.DataFrame([subtitulo_resg], columns=df_fact.columns), df_fact], ignore_index=True)


    #--Construye la tabla de Item
    df_item = pd.DataFrame(resg_item)
    subtitulo_item = ['DocNum','LineNum','AcctCode','SumApplied','Descrip']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)


    #--Crea el archivo de OPCH
    excel_path_fact = f'{date_download} - ORCT pago1 - 18910.xlsx'
    df_fact.to_excel(excel_path_fact, index=False)
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{date_download} - RCT4 Pago2 - 18910.xlsx'
    df_item.to_excel(excel_path_item, index=False)
    print(f'Archivo OPCH exportado a {excel_path_item}')

    send_mail_finan_ret18910(excel_path_item, excel_path_fact, date_download)

#--------------------------------------------------------------------------------------#

def XlsxResg19210Finan(data_resg, resg_item):
    #--Construye la tabla de Facturas
    df_fact = pd.DataFrame(data_resg)
    subtitulo_resg = ['DocNum','DocType','Series','CardCode','DocDate','TaxDate','DocDueDate','Referencia','Ref2','CashSum','CashAccount']
    df_fact = pd.concat([pd.DataFrame([subtitulo_resg], columns=df_fact.columns), df_fact], ignore_index=True)


    #--Construye la tabla de Item
    df_item = pd.DataFrame(resg_item)
    subtitulo_item = ['DocNum','LineNum','AcctCode','SumApplied','Descrip']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)


    #--Crea el archivo de OPCH
    excel_path_fact = f'{date_download} - ORCT pago1 - 19210.xlsx'
    df_fact.to_excel(excel_path_fact, index=False)
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{date_download} - RCT4 Pago2 - 19210.xlsx'
    df_item.to_excel(excel_path_item, index=False)
    print(f'Archivo OPCH exportado a {excel_path_item}')

    send_mail_finan_ret19210(excel_path_item, excel_path_fact, date_download)

#--------------------------------------------------------------------------------------#

def CreateProv(rut,name):
    try:
        with transaction.atomic():
            ProvType.objects.create(
                rut = rut,
                name = name,
                prov_sap = 'N/A',
                cta_sap = '999',
                prov_type = 'Proveedor',
            )
        return print(f'Prov creado - {rut} - Name: {name}\n')

    except Exception as e:
        print (f'{str(e)} {name} - {rut} - CreateProv\n')

#--------------------------------------------------------------------------------------#

def CreateDocFact(rut_prov,doc_num,doc_type,date_issue,total,iva):
    DocXml.objects.create(
        rut = rut_prov,
        doc_number = doc_num,
        doc_type = doc_type,
        date_issue = date_issue,
        date_exp = date_issue,
        total = total,
        iva = iva,
    )
    return print(rut_prov, rut_prov.name, doc_num, doc_type, date_issue, total, iva,'Documento guardado')

#--------------------------------------------------------------------------------------#

def CreateDocResg(rut_prov,doc_num,doc_type,date_issue,total_credito,total_retencion):
    DocXml.objects.create(
        rut = rut_prov,
        doc_number = doc_num,
        doc_type = doc_type,
        date_issue = date_issue,
        date_exp = date_issue,
        total = float(total_credito) + float(total_retencion),
        iva = 0,
    )
    return print(rut_prov, rut_prov.name, doc_num, doc_type, date_issue, 'Documento guardado')
   
#--------------------------------------------------------------------------------------#

def CreateItemFact17453(doc_number,item_name_ret,amount_ret):
    Item.objects.create(
        doc_number = doc_number,
        line_number = 2,
        item_name = item_name_ret,
        quantity = 1,
        amount = float(amount_ret),
    )

    return print(doc_number, item_name_ret,amount_ret, 'Item guardado')

#--------------------------------------------------------------------------------------#

def CreateItem(doc_number,line_number,item_name,quantity,amount):
    Item.objects.create(
        doc_number = doc_number,
        line_number = line_number,
        item_name = item_name,
        quantity = float(quantity),
        amount = float(amount),
    )

    print(doc_number, line_number, item_name,quantity,amount, 'Item guardado')

#--------------------------------------------------------------------------------------#

def CreateItemResg(doc_number,item_name,amount):
    Item.objects.create(
        doc_number = doc_number,
        line_number = 1,
        item_name = item_name,
        quantity = 1,
        amount = float(amount),
    )

    print(doc_number, item_name,amount, 'Item guardado')

#--------------------------------------------------------------------------------------#

def AdDataFact(desde,hasta,cuenta, doc_number):
    try:
        with transaction.atomic():
            AdData.objects.create(
                doc_number = doc_number,
                date_from = desde,
                date_until = hasta,
                account = cuenta,

            )
            return print(doc_number,desde, hasta, cuenta,'Aditional data save')
    except Exception as e:
        print(f'{str(e)} - No aditional data - {doc_number}')
#--------------------------------------------------------------------------------------#
