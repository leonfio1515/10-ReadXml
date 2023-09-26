from variables import *
import sys
import xml.etree.ElementTree as ET
from django.db import transaction
from processDoc import ProcessFact, ProcessResg
from dataFrame import DataFrameFactFinan,DataFrameRetFinan
#------------------------------------------------------------------#

def ProcessXml():

    #---Crea directorio para guardarlos logs
    log_path = os.path.join(folder_path, log_console)
    sys.stdout = open(log_path, "w")

    #--Creamos una lista con los archivos descargados
    xml_files = [
        file for file in os.listdir(folder_path)
        if file.endswith('.xml')
    ]
    print(f'En ejecucion\n')

    for xml_file in xml_files:
        ns = {'ns': 'http://cfe.dgi.gub.uy'}
        file_path = os.path.join(folder_path, xml_file)
        tree = ET.parse(file_path)
        root = tree.getroot()

        with transaction.atomic():
            for i in root.findall('.//ns:CFE_Adenda', namespaces=ns):
                rut = i.find('.//ns:RUCEmisor', namespaces=ns).text               

                if i.find('.//ns:TipoCFE', namespaces=ns).text == '111':
                    ProcessFact(i, ns, xml_file)
                    print(f'Fin de factura \n')

                elif i.find('.//ns:TipoCFE', namespaces=ns).text == '182':
                    ProcessResg(i, ns, xml_file)
                    print(f'Fin de resguardo \n')

                elif i.find('.//ns:TipoCFE', namespaces=ns).text == '112':
                    print(f'Tiene Nota de credito - {rut} - {xml_file}\n')
                    
    print("Proceso completo", today)


    DataFrameFactFinan()
    DataFrameRetFinan()
    sys.stdout.close()

ProcessXml()