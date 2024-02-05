import pandas as pd
from variables import *
import sys
import django
from sendMail import *

#--------------------------------------------------------------------------------------#

mail_activate = False

#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *

#--------------------------------------------------------------------------------------#

def tabla_fact(data_fact):
    df_fact = pd.DataFrame(data_fact)
    subtitulo_fact = ['Correlativo','Cod. Proveedor','DocType','F. Contabilizacion','F. Vencimiento','F. Documento','Nro. Referencia',	'Moneda','Serie','Correlativo','CtlAccount','Series', 'DocTotal', 'JrnlMemo']
    df_fact = pd.concat([pd.DataFrame([subtitulo_fact], columns=df_fact.columns), df_fact], ignore_index=True)
    return df_fact

def tabla_item(data_item):
    df_item = pd.DataFrame(data_item)
    subtitulo_item = ['Correlativo','Secuencia','Artículo','Saldo del documento (Moneda de documento)','OcrCode','OcrCode2','Moneda', 'ESTANDAR', 'Quantity','FreeTxt','WhsCode','U_FechaDesde','U_FechaHasta', 'DiscPrcent']
    df_item = pd.concat([pd.DataFrame([subtitulo_item], columns=df_item.columns), df_item], ignore_index=True)
    return df_item

#--------------------------------------------------------------------------------------#

def xlsx_fact_finan(data_fact_finan, data_item_finan, name):
    df_fact = tabla_fact(data_fact_finan)
    df_item = tabla_item(data_item_finan)

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

def xlsx_fact(data_fact, data_item, name):
    df_fact = tabla_fact(data_fact)
    df_item = tabla_item(data_item)

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
