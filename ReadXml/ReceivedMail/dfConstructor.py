

#--------------------------------------------------------------------------------------#

def Create_df_Fact(doc_num_fact, prov_num, doc_date):
    data_fact = {
        'DocNum': doc_num_fact,
        'CardCode': prov_num,
        'DocType': 'dDocument_Items',
        'DocDate': doc_date,
        'DocDueDate': doc_date,
        'TaxDate': doc_date,
        'NumAtCard': doc_num_fact,
        'DocCurrency': 'UYU',
        'FolioPrefixString': 'A',
        'FolioNumber': 0,
        'ControlAccount': 20003,
        'Series': 14,
    }
    return data_fact

def Create_df_item_Fact(doc_num_item,item_num,article,amount):
    data_item = {
        'ParentKey': doc_num_item,
        'LineNum': item_num,
        'ItemCode': article,
        'UnitPrice': amount,
        'COGSCostingCode': 'NULL',
        'COGSCostingCode2': 'F_236',
        'TaxCode': 'IVA_CTB',
        'DocCurrency': 'UYU',
    }    

    return data_item

#--------------------------------------------------------------------------------------#

def Create_df_resg_17453(doc_num_resg17453,account_prov_resg17453,doc_date_resg17453,item_17453):
    data_resg_17453 = {
        'DocNum': doc_num_resg17453,
        'DocType': 'rAccount',
        'Series': '79',
        'CardCode': account_prov_resg17453,
        'DocDate': doc_date_resg17453,
        'TaxDate': doc_date_resg17453,
        'DocDueDate': doc_date_resg17453,
        'CounterReference': doc_num_resg17453,
        'Reference2': doc_num_resg17453,
        'CashSum': item_17453,
        'CashAccount': '102210',
    }
    return data_resg_17453

def Create_df_item_resg_17453(doc_num_resg17453,account_prov_resg17453,amount_resg17453):
    resg_item_17453 = {
        'ParentKey': doc_num_resg17453,
        'LineNum': '1',
        'AccountCode': account_prov_resg17453,
        'SumPaid': amount_resg17453,
        'Decription': 'Resguardo',
    }
    return resg_item_17453

#--------------------------------------------------------------------------------------#

def Create_df_resg_19210(doc_num_resg19210,account_prov_resg19210,doc_date_resg19210,item_19210):
    data_resg_19210 = {
        'DocNum': doc_num_resg19210,
        'DocType': 'rAccount',
        'Series': '79',
        'CardCode': account_prov_resg19210,
        'DocDate': doc_date_resg19210,
        'TaxDate': doc_date_resg19210,
        'DocDueDate': doc_date_resg19210,
        'CounterReference': doc_num_resg19210,
        'Reference2': doc_num_resg19210,
        'CashSum': item_19210,
        'CashAccount': '102209',
    }
    return data_resg_19210

def Create_df_item_resg_19210(doc_num_resg19210,account_prov_resg19210,amount_resg19210):
    resg_item_19210 = {
        'ParentKey': doc_num_resg19210,
        'LineNum': '1',
        'AccountCode': account_prov_resg19210,
        'SumPaid': amount_resg19210,
        'Decription': 'Resguardo',
    }
    return resg_item_19210

#--------------------------------------------------------------------------------------#

def Create_df_resg_18910(doc_num_resg18910,account_prov_resg18910,doc_date_resg18910,item_18910):
    data_resg_18910 = {
        'DocNum': doc_num_resg18910,
        'DocType': 'rAccount',
        'Series': '79',
        'CardCode': account_prov_resg18910,
        'DocDate': doc_date_resg18910,
        'TaxDate': doc_date_resg18910,
        'DocDueDate': doc_date_resg18910,
        'CounterReference': doc_num_resg18910,
        'Reference2': doc_num_resg18910,
        'CashSum': item_18910,
        'CashAccount': '102208',
    }
    return data_resg_18910

def Create_df_item_resg_18910(doc_num_resg18910,account_prov_resg18910,amount_resg18910):
    resg_item_18910 = {
        'ParentKey': doc_num_resg18910,
        'LineNum': '1',
        'AccountCode': account_prov_resg18910,
        'SumPaid': amount_resg18910,
        'Decription': 'Resguardo',
    }
    return resg_item_18910

#--------------------------------------------------------------------------------------#

