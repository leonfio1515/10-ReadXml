from variables import *
import sys
import xml.etree.ElementTree as ET
from django.db import transaction
from processDoc import ProcessFact
from dataFrame import *
#------------------------------------------------------------------#

def ProcessXml():
    with open(log_path, "w") as log_file:
        sys.stdout = log_file

        xml_files = [
            file for file in os.listdir(output_folder)
            if file.endswith(file_format)
        ]

        for xml_file in xml_files:
            try:
                ns = {'ns': 'http://cfe.dgi.gub.uy'}
                file_path = os.path.join(output_folder, xml_file)
                tree = ET.parse(file_path)
                root = tree.getroot()

                with transaction.atomic():
                    for i in root.findall('.//ns:CFE_Adenda', namespaces=ns):
                        rut = i.find('.//ns:RUCEmisor', namespaces=ns).text  
                        type_doc = i.find('.//ns:TipoCFE', namespaces=ns).text             

                        if type_doc == '111':
                            ProcessFact(i, ns, xml_file)
                            print(f'Fin de factura \n')

            except Exception as e:
                print('ERROR', str(e), xml_file)

        print("Proceso completo", today)
        

        # DataFrameFactFinan()
        # DataFrameRetFinan()

ProcessXml()