import os
import sys
import django

from function import *
from dfConstructor import *
from query import *
#-----------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#

def DataFrameFactFinan():
    for index, fact in enumerate(factsFinan):
        try:
            prov_num.append(fact.rut.prov_sap)
            doc_num_fact.append(fact.doc_number)
            doc_date.append(fact.date_issue.strftime('%Y%m%d'))
            items = Item.objects.filter(doc_number=fact)

        except Exception as e:
            print(f'{str(e)} - Prov: {fact.rut.prov_sap} - Doc: {fact.doc_number} - DF FactFinan')


        for index_item, item in enumerate(items):
            if item.item_name == ticket:
                pass
            else:
                doc_num_item.append(item.doc_number.doc_number)
                item_num.append(item.line_number)
                amount.append(item.amount)

                try:
                    art = Article.objects.get(name__icontains=item.doc_number.rut)
                except Exception as e:
                    print(f'{str(e)} - Prov: {item.doc_number.rut} - Item: {item.item_name} - Doc: {item.doc_number.doc_number} - DF FactFinan' )

                try:
                    if item.item_name == retencion:
                        article.append(ret_cod)
                    elif item.item_name == cost_envio:
                        article.append(cost_cod)
                    elif item.item_name == financiacion:
                        article.append(finan_cod)
                    else:
                        article.append(art.cod_sap)
                except Exception as e:
                    print(f'{str(e)} - DF FactFinan')


    data_fact = Create_df_Fact(doc_num_fact, prov_num, doc_date)
    data_item = Create_df_item_Fact(doc_num_item,item_num,article,amount)

    XlsxFactFinan(data_fact, data_item)

def DataFrameRetFinan():
    for index, resg in enumerate(resgsFinan):
        items = Item.objects.filter(doc_number=resg)
        for index_item, item in enumerate(items):           

            if item.item_name == '2183161' or item.item_name == '2183169':

                try:
                    doc_num_resg17453.append(resg.doc_number)
                    doc_date_resg17453.append(resg.date_issue.strftime('%Y%m%d'))
                    account_prov_resg17453.append(resg.rut.cta_sap)
                    amount_resg17453.append(resg.total)
                    item_17453.append(item.amount)

                    data_resg17453 = Create_df_resg_17453(doc_num_resg17453,account_prov_resg17453,doc_date_resg17453,item_17453)
                    resg_item17453 = Create_df_item_resg_17453(doc_num_resg17453,account_prov_resg17453,amount_resg17453)
                except Exception as e:
                    print(f'{str(e)} - Doc: {resg.doc_number} - Prov: {resg.rut.cta_sap} - DF RetFinan')

            elif item.item_name == '2181411' or item.item_name == '2181415':
                try:
                    doc_num_resg19210.append(resg.doc_number)
                    doc_date_resg19210.append(resg.date_issue.strftime('%Y%m%d'))
                    account_prov_resg19210.append(resg.rut.cta_sap)
                    amount_resg19210.append(resg.total)
                    item_19210.append(item.amount)

                    data_resg19210 = Create_df_resg_19210(doc_num_resg19210,account_prov_resg19210,doc_date_resg19210,item_19210)
                    resg_item19210 = Create_df_item_resg_19210(doc_num_resg19210,account_prov_resg19210,amount_resg19210)
                except Exception as e:
                    print(f'{str(e)} - Doc: {resg.doc_number} - Prov: {resg.rut.cta_sap} - DF RetFinan')

            elif item.item_name == '2183166':
                try:
                    doc_num_resg18910.append(resg.doc_number)
                    doc_date_resg18910.append(resg.date_issue.strftime('%Y%m%d'))
                    account_prov_resg18910.append(resg.rut.cta_sap)
                    amount_resg18910.append(resg.total)
                    item_18910.append(item.amount)

                    data_resg18910 = Create_df_resg_18910(doc_num_resg18910,account_prov_resg18910,doc_date_resg18910,item_18910)
                    resg_item18910 = Create_df_item_resg_18910(doc_num_resg18910,account_prov_resg18910,amount_resg18910)
                except Exception as e:
                    print(f'{str(e)} - Doc: {resg.doc_number} - Prov: {resg.rut.cta_sap} - DF RetFinan')

    try:
        XlsxResg19210Finan(data_resg19210, resg_item19210)
    except Exception as e:
        print(f'{str(e)} - No existe resguardo - In resg 19210')
    try:
        XlsxResg18910Finan(data_resg18910, resg_item18910)
    except Exception as e:
        print(f'{str(e)} - No existe resguardo  - In resg 18910')
    try:
        XlsxResg17453Finan(data_resg17453, resg_item17453)
    except Exception as e:
        print(f'{str(e)} - No existe resguardo - In resg 17453')

#--------------------------------------------------------------#
