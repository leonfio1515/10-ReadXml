import sys
import django
from variables import *
from function import *
#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#
#--------------------------------------------------------------------------------------#

def ProcessFact(i, ns, xml_file):
    try:       
        rut = i.find('.//ns:RUCEmisor', namespaces=ns)
        name = i.find('.//ns:RznSoc', namespaces=ns)
        doc_num = i.find('.//ns:Nro', namespaces=ns)
        doc_type = i.find('.//ns:TipoCFE', namespaces=ns)
        date_issue = i.find('.//ns:FchEmis', namespaces=ns)
        total = i.find('.//ns:MntPagar', namespaces=ns)
        iva = i.find('.//ns:MntIVATasaBasica', namespaces=ns)
        data = i.find('.//ns:Detalle', namespaces=ns)
    
        if all (elem is not None for elem in [rut, doc_num, doc_type, date_issue, total, iva,name]):
            rut = rut.text
            doc_num = doc_num.text
            doc_type = doc_type.text
            date_issue = date_issue.text
            total = total.text
            iva = iva.text                        
            name = name.text                        

        try:
            CreateProv(rut, name)
            rut_prov = ProvType.objects.get(rut=rut)

        except Exception as e:
            print(f'{str(e)} - {rut} - {name} - ProcessFact')

        try:
            CreateDocFact(rut_prov,doc_num,doc_type,date_issue,total,iva)
            doc_number = DocXml.objects.get(doc_number=doc_num)

            items = data.findall('.//ns:Item', namespaces=ns)

            for e in items:
                if  e.find('.//ns:RetencPercep', namespaces=ns):
                    item_name_ret = e.find('.//ns:CodRet', namespaces=ns)
                    amount_ret = e.find('.//ns:ValRetPerc', namespaces=ns)
                    line_number = e.find('.//ns:NroLinDet', namespaces=ns)
                    item_name = e.find('.//ns:NomItem', namespaces=ns)
                    quantity = e.find('.//ns:Cantidad', namespaces=ns)
                    amount = e.find('.//ns:MontoItem', namespaces=ns)

                    if all (el is not None for el in [item_name_ret, amount_ret,line_number, item_name, quantity, amount]):
                        item_name_ret = item_name_ret.text
                        amount_ret = amount_ret.text
                        line_number = line_number.text
                        item_name = item_name.text
                        quantity = quantity.text
                        amount = amount.text

                        print('17453 en Factura')
                        print(item_name_ret, amount_ret , 'RESGUARDO')

                        try:
                            CreateItemFact17453(doc_number,item_name_ret,amount_ret)
                            CreateItem(doc_number,line_number,item_name,quantity,amount)

                        except ProvType.DoesNotExist:
                            print(f'Num doc no encontrado {doc_number} en {xml_file} - ProcessFact')

                else:
                    line_number = e.find('.//ns:NroLinDet', namespaces=ns)
                    item_name = e.find('.//ns:NomItem', namespaces=ns)
                    quantity = e.find('.//ns:Cantidad', namespaces=ns)
                    amount = e.find('.//ns:MontoItem', namespaces=ns)

                    if all (el is not None for el in [line_number, item_name, quantity, amount]):
                        line_number = line_number.text
                        item_name = item_name.text
                        quantity = quantity.text
                        amount = amount.text

                        try:
                            CreateItem(doc_number,line_number,item_name,quantity,amount)

                        except ProvType.DoesNotExist:
                            print(f'Num doc no encontrado {doc_number} en {xml_file} - ProcessFact')

            try:
                desde = i.find('.//ns:PeriodoDesde', namespaces=ns).text
                hasta = i.find('.//ns:PeriodoHasta', namespaces=ns).text
                cuenta = i.find('.//ns:InfoAdicional', namespaces=ns).text
                AdDataFact(desde,hasta,cuenta, doc_number)
            except Exception as e:
                print(f'{str(e)} - Datos no encontrados en {doc_num} - ProcessFact')

        except ProvType.DoesNotExist:
            print(f'Rut no encontrado {rut} en {xml_file} - ProcessFact')

    except Exception as e:
        print(f'Error al procesar el archivo {xml_file}: {str(e)} - ProcessFact')

#--------------------------------------------------------------------------------------#

def ProcessResg(i, ns, xml_file):
    try:       
        rut = i.find('.//ns:RUCEmisor', namespaces=ns)
        name = i.find('.//ns:RznSoc', namespaces=ns)
        doc_num = i.find('.//ns:Nro', namespaces=ns)
        doc_type = i.find('.//ns:TipoCFE', namespaces=ns)
        date_issue = i.find('.//ns:FchEmis', namespaces=ns)
        total_credito = i.find('.//ns:MntTotCredFisc', namespaces=ns)
        total_retencion = i.find('.//ns:MntTotRetenido', namespaces=ns)
        data = i.find('.//ns:Totales', namespaces=ns)

        if all (ele is not None for ele in [rut, doc_num, doc_type, date_issue,total_retencion,total_credito,name]):
            rut = rut.text
            name = name.text
            doc_num = doc_num.text
            doc_type = doc_type.text
            date_issue = date_issue.text
            total_credito = total_credito.text
            total_retencion = total_retencion.text

            try:
                CreateProv(rut, name)
                rut_prov = ProvType.objects.get(rut=rut)
            except Exception as e:
                print(f'{str(e)} - ProcessResg')

            try:
                CreateDocResg(rut_prov,doc_num,doc_type,date_issue,total_credito,total_retencion)
                doc_number = DocXml.objects.get(doc_number=doc_num)

                items = data.findall('.//ns:RetencPercep', namespaces=ns)
                
                for e in items:
                    item_name = e.find('.//ns:CodRet', namespaces=ns)
                    amount = e.find('.//ns:ValRetPerc', namespaces=ns)

                    if all (el is not None for el in [item_name, amount]):
                        item_name = item_name.text
                        amount = amount.text

                        try:
                            CreateItemResg(doc_number,item_name,amount)

                        except ProvType.DoesNotExist:
                            print(f'Num doc no encontrado {doc_number} en {xml_file} - ProcessResg\n')

            except ProvType.DoesNotExist:
                print(f'Rut no encontrado {rut} en {xml_file} - ProcessResg\n')

    except Exception as e:
        print(f'Error al procesar el archivo {xml_file}: {str(e)} - ProcessResg\n')    

