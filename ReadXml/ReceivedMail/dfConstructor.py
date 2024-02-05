

def create_df_fact(doc_num_fact_var, prov_num_fact_var, doc_date_fact_var, doc_date_exp_fact_var, currency_fact_var, amount_fact_var, memo_fact_var, control_accoun_var):
    data_fact = {
        'DocNum': doc_num_fact_var,
        'CardCode': prov_num_fact_var,
        'DocType': 'dDocument_Items',
        'DocDate': doc_date_fact_var,
        'DocDueDate': doc_date_exp_fact_var,
        'TaxDate': doc_date_fact_var,
        'NumAtCard': doc_num_fact_var,
        'DocCurrency': currency_fact_var,
        'FolioPrefixString':'A',
        'FolioNumber':0,
        'ControlAccount': control_accoun_var,
        'Series': 14,
        'DocTotal': amount_fact_var,
        'JournalMemo': memo_fact_var,
    }
    return data_fact

def create_df_item_fact(doc_num_item_fact_var,item_num_fact_var,article_fact_var,amount_item_fact_var,norm_fact_var,tax_type_fact_var,currency_item_fact_var, quantity_fact_var,wHouse_fact_var, date_from_fact_var, date_until_fact_var, desc_item_fact_var, norm_f_fact_var,free_text_fact_var):
    data_item = {
        'ParentKey': doc_num_item_fact_var,
        'LineNum': item_num_fact_var,
        'ItemCode': article_fact_var,
        'UnitPrice': amount_item_fact_var,
        'COGSCostingCode': norm_fact_var,
        'COGSCostingCode2': norm_f_fact_var,
        'TaxCode': tax_type_fact_var,
        'DocCurrency': currency_item_fact_var,
        'Quantity': quantity_fact_var,
        'FreeText': free_text_fact_var,
        'WarehouseCode': wHouse_fact_var,
        'U_FechaDesde': date_from_fact_var,
        'U_FechaHasta': date_until_fact_var,
        'DiscountPercent': desc_item_fact_var,
    }    

    return data_item
