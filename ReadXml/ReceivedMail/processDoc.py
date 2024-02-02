import sys
import django
from variables import *
from function import *
import xml.etree.ElementTree as ET
#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
def GetProv(i, ns):
    try:
        rut = i.find('.//ns:RUCEmisor', namespaces=ns).text
        name = i.find('.//ns:RznSoc', namespaces=ns).text
    except Exception as e:
        print(f'Error al obtener datos del proveedor (Fun GetProv) - {str(e)}')
    return rut, name

def GetDocXml(i, ns):
    try:
        cod_doc = i.find('.//ns:FmaPago', namespaces=ns).text
        doc_num = i.find('.//ns:Nro', namespaces=ns).text
        doc_type = i.find('.//ns:TipoCFE', namespaces=ns).text
        date_issue = i.find('.//ns:FchEmis', namespaces=ns).text
        try:
            date_exp = i.find('.//ns:FchVenc', namespaces=ns).text
        except:
            date_exp = date_issue
        total = i.find('.//ns:MntPagar', namespaces=ns).text
        try:
            iva = i.find('.//ns:MntIVATasaBasica', namespaces=ns).text
        except:
            iva = 0
        try:
            iva_min = i.find('.//ns:MntIVATasaMin', namespaces=ns).text
        except:
            iva_min = 0
        currency_type = i.find('.//ns:TpoMoneda', namespaces=ns).text
        return doc_num, doc_type, date_issue, date_exp, total, iva, iva_min, currency_type, cod_doc
    
    except Exception as e:
        print(f'Error al obtener valores DocXml {i}-{ns} (Fun GetDocXml) - {str(e)}')  

def GetAdenda(i, ns, rut):
    rut = i.find('.//ns:RUCEmisor', namespaces=ns).text
    try:
        if rut == '211962820014':
            try:
                adenda = i.find('.//ns:Adenda', namespaces=ns).text
                adenda_tree = ET.fromstring(adenda)
                consumo_txt = adenda_tree.find('.//totalUsage').text
                if consumo_txt == '0.0':
                    consumo = 1
                else:
                    consumo = float(consumo_txt)
            except:
                consumo = 1
        else:                    
            try:
                consumo = i.find('.//cabezaldetalle/consumo_tot_act').text
                if consumo == '0':
                    consumo = '1'
            except:
                consumo = i.find('.//panelizquierdo/consumo_tot_act').text
                if consumo == '0':
                    consumo = '1'      
    except:
        consumo = '1'    

    return consumo

def GetItemRet(i, ns, e):
    try:
        try:
            item_name_ret = e.find('.//ns:CodRet', namespaces=ns).text
        except:
            item_name_ret = ''

        try:
            amount_ret = e.find('.//ns:ValRetPerc', namespaces=ns).text
        except:
            amount_ret = ''

        try:
            line_number = e.find('.//ns:NroLinDet', namespaces=ns).text
        except:
            line_number = ''

        try:
            item_name = e.find('.//ns:NomItem', namespaces=ns).text
        except:
            item_name = ''

        try:
            quantity = e.find('.//ns:Cantidad', namespaces=ns).text
        except:
            quantity = ''

        try:
            amount = e.find('.//ns:MontoItem', namespaces=ns).text
        except:
            amount = ''

        try:
            iva_type = e.find('.//ns:IndFact', namespaces=ns).text
        except:
            iva_type = ''

        try:
            consumo = i.find('.//ns:consumo_tot_act', namespaces=ns).text
        except:
            consumo = ''

        try:
            cod = i.find('.//ns:CodRet', namespaces=ns).text
        except:
            cod = ''

        try:
            try:
                desc = e.find('.//ns:DescuentoPct', namespaces=ns).text
            except:
                desc = i.find('.//ns:GlosaDR', namespaces=ns).text
        except:
            desc = 0    
    except Exception as e:
        print(f'Error al obtener item retencion (Fun GetItemRet) - {str(e)}')

    return item_name_ret, amount_ret, line_number, item_name, quantity, amount, iva_type, consumo, cod, desc

def GetItem(i, ns, e):
    try:
        rut = i.find('.//ns:RUCEmisor', namespaces=ns).text
        line_number = e.find('.//ns:NroLinDet', namespaces=ns).text
        item_name = e.find('.//ns:NomItem', namespaces=ns).text
        quantity = e.find('.//ns:Cantidad', namespaces=ns).text
        iva_type = e.find('.//ns:IndFact', namespaces=ns).text

        try:
            if rut == '216639270017':
                cod = e.find('.//ns:DscItem', namespaces=ns).text
            else:
                cod = i.find('.//ns:Cod', namespaces=ns).text
        except:
            cod = ''
        amount = e.find('.//ns:MontoItem', namespaces=ns).text

        try:
            desc_g = e.find('.//ns:DescuentoPct', namespaces=ns).text
            if desc_g == '0.00':
                try:
                    desc = i.find('.//ns:GlosaDR', namespaces=ns).text
                except Exception as e:
                    desc = 0
            else:
                desc = desc_g

        except Exception as e:
            desc = 0
    except Exception as e:
        print(f'Error al obtener valores de Item {rut} - (Fun GetItem) - {str(e)}')

    return line_number, item_name, quantity, iva_type, cod, amount, desc

def GetAddData(i, ns, rut, date_issue):
    try:
        rut = i.find('.//ns:RUCEmisor', namespaces=ns).text
        try:
            add_data = i.find('.//ns:Adenda', namespaces=ns).text         
            if rut == '211677550012' or rut == '211383670010':
                match = re.search(r'Contrato: (\d+)', add_data)
                if match:
                    cuenta = match.group(1)
            elif rut == '080073770017':
                match_cod = re.search(r'Afiliado: (\d+)', add_data)
                match_type = re.search(r'Cantidad de (\w+)', add_data)
                if match_cod and match_type:
                    cuenta = f'{match_cod.group(1)} - {match_type.group(1)}'

            elif rut == '213108740018':
                ns2 = {'ns2': 'http://tilsor.com.uy/#AndaAdenda'}
                data_linea = i.findall('.//ns2:datosExtraAnda/ns2:lstLineas/ns2:linea',namespaces=ns2)
                add_data = data_linea[0].text
                match = re.search(r'COM (\d+)', add_data)
                if match:
                    cuenta = match.group(1)

            elif rut in ['214111700011', '218878260019']:
                info_add = i.find('.//ns:Adenda', namespaces=ns).text         
                match = re.search(r'Nro. de Usuario: (\d+)', info_add)
                if match:
                    cuenta = match.group(1)

            elif rut == '211962820014':
                info_add = i.find('.//ns:InfoAdicional', namespaces=ns).text         
                match = re.search(r'Cuenta: (\d+)', info_add)
                if match:
                    cuenta = match.group(1)
            elif rut == '215166390012':
                info_add = i.find('.//ns:InfoAdicional', namespaces=ns).text         
                cuenta = info_add
            else:
                cuenta = i.find('.//ns:InfoAdicional', namespaces=ns).text
        except:
            if rut == '213074330017':
                try:
                    cuenta = i.find('.//ns:Adenda', namespaces=ns).text
                except:
                    cuenta = i.find('.//ns:RznSocRecep', namespaces=ns).text
            else:
                cuenta = 'Null'

        try:
            try:
                desde = i.find('.//ns:PeriodoDesde', namespaces=ns).text
            except Exception as e:
                date = i.find('.//periodoconsumo', namespaces=ns).text
                date = date.split()[0]
                date = datetime.strptime(date, '%d/%m/%Y')
                date = date.strftime('%Y-%m-%d')
                desde = date
                print(str(e), 'Error Desde')
        except Exception as e:
            desde = date_issue

        try:
            try:
                hasta = i.find('.//ns:PeriodoHasta', namespaces=ns).text
            except Exception as e:
                date = i.find('.//periodoconsumo', namespaces=ns).text
                date = date.split()[2]
                date = datetime.strptime(date, '%d/%m/%Y')
                date = date.strftime('%Y-%m-%d')
                hasta = date
        except Exception as e:
            hasta = date_issue
            date = i.find('.//ns:Nro', namespaces=ns).text


        try:
            lectura_ant = i.find('.//ns:consumo_tot_act', namespaces=ns).text
        except:
            lectura_ant = 1
        try:
            lectura_act = i.find('.//ns:consumo_tot_act', namespaces=ns).text
        except:
            lectura_act = 1
    except Exception as e:
        print(f'Error al obtener datos adicionales {rut} (Fun GetAddData) - {str(e)}')

    return cuenta, desde, hasta, lectura_ant, lectura_act


def ProcessFact(i, ns, xml_file):


    rut, name = GetProv(i, ns)        
    doc_num, doc_type, date_issue, date_exp, total, iva, iva_min, currency_type, cod_doc = GetDocXml(i, ns)
    consumo = GetAdenda(i, ns, rut)
    sobre = xml_file

    try:
        get_doc = DocXml.objects.get(doc_number = doc_num)
        print(f'El documento {get_doc.doc_number} del sobre {xml_file} ya existe')
    
    except DocXml.DoesNotExist:

        try:
            get_prov = ProvType.objects.get(rut=rut)
            print(f'El proveedor {get_prov.rut} - {get_prov.name} ya existe')
        except ProvType.DoesNotExist:
            try:
                CreateProv(rut, name)
                rut_prov = ProvType.objects.get(rut=rut)
            except Exception as e:
                print(f'Error al crear el proveedor (Fun CreateProv): {rut} - {name} - {str(e)}')
        except Exception as e:
            print(f'Error: {str(e)} - {rut} - {name}')

        items = i.findall('.//ns:Item', namespaces=ns)


        try:
            item_name_search = i.find('.//ns:NomItem', namespaces=ns).text
            if item_name_search != 'Cobranza':   

                rut_prov = ProvType.objects.get(rut=rut)
                CreateDocFact(rut_prov,doc_num,doc_type,date_issue,total,iva,currency_type,iva_min, date_exp, cod_doc, sobre)
                doc_number = DocXml.objects.get(doc_number=doc_num)

                for e in items:

                    if  e.find('.//ns:RetencPercep', namespaces=ns):

                        item_name_ret, amount_ret, line_number, item_name, quantity, amount, iva_type, consumo, cod, desc = GetItemRet(i, ns, e)

                        try:
                            CreateItemFact17453(doc_number, line_number, item_name_ret, quantity, amount_ret, iva_type, cod, desc)
                        except ProvType.DoesNotExist:
                            print(f'Num doc no encontrado al crear ItemFact17453 con Resg {doc_number} en {xml_file}')

                        try:
                            CreateItem(rut, doc_number, line_number, item_name, quantity, amount, iva_type, cod, desc)
                        except ProvType.DoesNotExist:
                            print(f'Num doc no encontrado al crear ItemFact con Resg {doc_number} en {xml_file}')
                    else:
                        line_number, item_name, quantity, iva_type, cod, amount, desc = GetItem(i, ns, e)
                        try:
                            CreateItem(rut, doc_number, line_number, item_name, quantity, amount, iva_type, cod, desc)

                        except ProvType.DoesNotExist:
                            print(f'Num doc no encontrado al crear ItemFact {doc_number} en {xml_file}')


                try:
                    cuenta, desde, hasta, lectura_ant, lectura_act = GetAddData(i, ns, e, date_issue)
                    AdDataFact(desde,hasta,cuenta, doc_number,consumo, lectura_act, lectura_ant)
                except Exception as e:
                    print(f'Datos no encontrados en {doc_num} - {str(e)}')

            else:
                print(f'Documento no guardado - Factura Cobranza' - {doc_num})

        except ProvType.DoesNotExist:
            print(f'Rut no encontrado {rut} en {xml_file}')

    except Exception as e:
        print(f'Error al procesar el archivo (Factura) {xml_file}: {str(e)}')

        
