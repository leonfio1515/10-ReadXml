import pandas as pd
from variables import *
import sys
import django
from sendMail import *

#--------------------------------------------------------------------------------------#

mail_activate = True

#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *

#--------------------------------------------------------------------------------------#

def tablaFact(data_fact):
    df_fact = pd.DataFrame(data_fact)
    subtitulo_fact = ['Correlativo','Cod. Proveedor','DocType','F. Contabilizacion','F. Vencimiento','F. Documento','Nro. Referencia',	'Moneda','Serie','Correlativo','CtlAccount','Series', 'DocTotal', 'JrnlMemo']
    df_fact = pd.concat([pd.DataFrame([subtitulo_fact], columns=df_fact.columns), df_fact], ignore_index=True)
    return df_fact

def tablaItem(data_item):
    df_item = pd.DataFrame(data_item)
    subtitulo_item = ['Correlativo','Secuencia','Artículo','Saldo del documento (Moneda de documento)','OcrCode','OcrCode2','Moneda', 'ESTANDAR', 'Quantity','FreeTxt','WhsCode','U_FechaDesde','U_FechaHasta', 'DiscPrcent']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)
    return df_item

#--------------------------------------------------------------------------------------#

def XlsxFactFinan(data_fact_finan, data_item_finan, name):
    df_fact = tablaFact(data_fact_finan)
    df_item = tablaItem(data_item_finan)

    #--Crea el archivo de OPCH
    excel_path_fact = f'{output_folder}/{date_process} - {name} - OPCH Factura1.csv'
    df_fact.to_csv(excel_path_fact, index=False, sep=',')
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{output_folder}/{date_process} - {name} - PCH1 Factura2.csv'
    df_item.to_csv(excel_path_item, index=False, sep=',')
    document_type = 'Facturas Financieras'
    print(f'Archivo OPCH exportado a {excel_path_item}')

    if mail_activate:
        send_mail_finan(excel_path_item, excel_path_fact, date_from_download,document_type)

#--------------------------------------------------------------------------------------#

def XlsxFact(data_fact, data_item, name):
    df_fact = tablaFact(data_fact)
    df_item = tablaItem(data_item)

    #--Crea el archivo de OPCH
    excel_path_fact = f'{output_folder}/{date_process} - {name} - OPCH Factura1.csv'
    df_fact.to_csv(excel_path_fact, index=False, sep=',')
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{output_folder}/{date_process} - {name} - PCH1 Factura2.csv'
    df_item.to_csv(excel_path_item, index=False, sep=',')
    document_type = f'Facturas {name}'
    print(f'Archivo OPCH exportado a {excel_path_item}')

    if mail_activate:
        send_mail_prov_fact(excel_path_item, excel_path_fact, date_from_download,document_type)

#--------------------------------------------------------------------------------------#

    #--Construye la tabla de Facturas
    df_fact = pd.DataFrame(data_resg)
    subtitulo_resg = ['DocNum','DocType','Series','CardCode','DocDate','TaxDate','DocDueDate','Referencia','Ref2','CashSum','CashAccount']
    df_fact = pd.concat([pd.DataFrame([subtitulo_resg], columns=df_fact.columns), df_fact], ignore_index=True)


    #--Construye la tabla de Item
    df_item = pd.DataFrame(resg_item)
    subtitulo_item = ['DocNum','LineNum','AcctCode','SumApplied','Descrip']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)


    #--Crea el archivo de OPCH
    excel_path_fact = f'{output_folder}/{date_process} - ORCT pago1 - 19210.csv'
    df_fact.to_csv(excel_path_fact, index=False, sep=',')
    print(f'Archivo OPCH exportado a {excel_path_fact}')

    #--Crea el archivo de PCH1
    excel_path_item = f'{output_folder}/{date_process} - RCT4 Pago2 - 19210.csv'
    df_item.to_csv(excel_path_item, index=False, sep=',')
    document_type = 'Resguardo 19210'
    print(f'Archivo OPCH exportado a {excel_path_item}')

    if mail_activate:
        send_mail_finan(excel_path_item, excel_path_fact, date_from_download,document_type)