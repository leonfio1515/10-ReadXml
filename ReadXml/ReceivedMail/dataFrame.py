import os
import sys
import django
import re

from django.db.models import Sum
from function import *
from dfConstructor import *
from xlsConstructor import *
from query import *
#-----------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#

#--------------------------------------------------------------#

def data_frame_fact_finan():
    with open(log_df_finan_fact_path, "w") as log_file_finan_fact:
        sys.stdout = log_file_finan_fact


        excluir = ('Comisiones por servicios financieros','COMISIONES POR SERVICIOS FINANCIEROS')
        name = 'Financieras'
        try:
            for index, fact in enumerate(factsFinan):
                item_line = 1
                items = Item.objects.filter(doc_number=fact)

                if items[0].item_name in excluir:
                    pass
                else:
                    try: 
                        get_doc_fact(fact.doc_number, 
                                        fact.rut.prov_sap, 
                                        fact.date_issue, 
                                        fact.date_exp, 
                                        fact.currency, 
                                        fact.rut.control_account, 
                                        fact.total, 
                                        fact.rut.name)
                        items = Item.objects.filter(doc_number=fact)           
                    except Exception as e:
                        print(f'{str(e)} - Prov: {fact.rut.prov_sap} - Doc: {fact.doc_number}')


                    for index_item, item in enumerate(items):
                        if item.item_name == ticket or item.sub_amount <= 0:
                            pass
                        else:
                            norm_f = 'F_236'
                            whouse = ''
                            date_from = ''
                            date_until = ''
                            desc = ''
                            tax = get_iva_type(item)
                            norm_g = get_norm_finan(item)
                            item_amount = get_item_amount_finan(fact, item, tax)
                            free_text = fact.rut.name
                            quantity = 1
                            
                            try:
                                art_id = Article.objects.get(name__icontains=item.doc_number.rut)
                            except Exception as e:
                                print(f'{str(e)} - Prov: {item.doc_number.rut} - Item: {item.item_name} - Doc: {item.doc_number.doc_number}' )

                            art = get_item_finan(item, art_id)

                        get_item_fact(   item.doc_number.doc_number, 
                                            item_line, 
                                            art, 
                                            item_amount, 
                                            norm_g, 
                                            norm_f, 
                                            fact.currency, 
                                            tax, 
                                            quantity, 
                                            whouse, 
                                            fact.date_issue, 
                                            fact.date_issue, 
                                            desc, 
                                            free_text 
                                            )

                        item_line += 1
                    print(f'Factura de Financieras creada - Finan: {fact.rut.name} - Doc: {fact.doc_number} - Date: {fact.date_issue} - Create: {fact.date_create} - Sobre: {fact.sobre}\n')

            try:
                data_fact_finan = create_df_fact(
                        doc_num_fact_var, 
                        prov_num_fact_var, 
                        doc_date_fact_var, 
                        doc_date_exp_fact_var, 
                        currency_fact_var, 
                        amount_fact_var, 
                        memo_fact_var,
                        control_accoun_var
                    )
                
                data_item_finan = create_df_item_fact(
                    doc_num_item_fact_var,
                    item_num_fact_var,
                    article_fact_var,
                    amount_item_fact_var,
                    norm_fact_var,
                    tax_type_fact_var,
                    currency_item_fact_var,
                    quantity_fact_var,
                    wHouse_fact_var, 
                    date_from_fact_var, 
                    date_until_fact_var, 
                    desc_item_fact_var, 
                    norm_f_fact_var,
                    free_text_fact_var
                    )
                print(data_fact_finan)
            except Exception as e:
                print(str(e))

            xlsx_fact_finan(data_fact_finan, data_item_finan, name)
            clear_list()

        except:
            print('No existen facturas de Financieras')
    sys.stdout = sys.__stdout__

#--------------------------------------------------------------#

def data_frame_fact_ute():
    excluir = r'Saldos a Favor'
    try:
        for index, fact in enumerate(factsUte):
            try:
                name = 'UTE'
                add_data = AdData.objects.get(doc_number=fact)
                consumo = add_data.cons_lect.replace(',','.')
                account = add_data.account

                try:
                    suc_id = 'Null'
                    suc = 'Null'
                except Exception as e:
                    if account == '0655141000':
                        suc = '026'
                    elif account == '1813951000' or account == '4140591000' :
                        suc = '069'
                    else:
                        suc = 'Null'
                memo = f'Suc: {suc} - {add_data.date_from} - {add_data.date_until} - {consumo} Kw'

                get_doc_fact(fact.doc_number, fact.rut.prov_sap, fact.date_issue, fact.date_exp, fact.currency, fact.rut.control_account, fact.total, memo)

                items = Item.objects.filter(doc_number=fact)
            except Exception as e:
                print(f'{str(e)} - Prov: {fact.rut.prov_sap} - Doc: {fact.doc_number}')

            for index_item, item in enumerate(items):
                try:
                    coin = re.search(excluir, item.item_name)

                    if coin or item.sub_amount == 0:
                        pass
                    elif item.sub_amount > 0:
                        try: 
                            imp_unit = round(float(item.sub_amount),2)
                        except Exception as e:
                            imp_unit = 0
                            print(str(e))

                        if imp_unit != 0:                    
                            imp_unit = get_item_amount_ute(item, add_data)
                            cant_unit = '1'                       
                            desc = round(float(item.desc_porc),2)
                            tax = get_iva_type(item)
                            norm_g, norm_f, whouse = get_norm_ute(add_data, account)
                            art = get_art(item, name)
                            free_text = ''

                        get_item_fact(item.doc_number.doc_number,item.line_number, art, imp_unit, norm_g, norm_f, fact.currency, tax, cant_unit, whouse, add_data.date_from, add_data.date_until, desc, free_text )

                except Exception as e:
                    print(f'{str(e)} - Prov: {fact.rut.prov_sap} - Doc: {fact.doc_number}')
            print(f'Factura de UTE creada - Doc: {fact.doc_number} - Date: {fact.date_issue} - Create: {fact.date_create} - Sobre: {fact.sobre}')
    except:
        print('No existen documentos de UTE')
    print('Fin facturas UTE\n')
#--------------------------------------------------------------#

#----------------------------------------------------------------------------#

def process_data_frame():
    with open(log_df_prov_path, "w") as log_file_prov:
        sys.stdout = log_file_prov

        data_frame_fact_ute()
        name = 'Doc Proveedores'
        data_fact = create_df_fact(
                doc_num_fact_var, 
                prov_num_fact_var, 
                doc_date_fact_var, 
                doc_date_exp_fact_var, 
                currency_fact_var, 
                amount_fact_var, 
                memo_fact_var,
                control_accoun_var
            )

        data_item = create_df_item_fact(
            doc_num_item_fact_var,
            item_num_fact_var,
            article_fact_var,
            amount_item_fact_var,
            norm_fact_var,
            tax_type_fact_var,
            currency_item_fact_var,
            quantity_fact_var,
            wHouse_fact_var, 
            date_from_fact_var, 
            date_until_fact_var, 
            desc_item_fact_var, 
            norm_f_fact_var,
            free_text_fact_var
            )

        xlsx_fact(data_fact, data_item, name)
        clear_list()    
    sys.stdout = sys.__stdout__

#--------------------------------------------------------------#

