import os
import win32com.client
import sys
import re
from variables import *

from processXml import ProcessXml
from Model.models import DocXml
#--------------------------------------------------------------#


def SaveMail():      

    #--Crea directorio para guardar los mail descargados
    output_folder.mkdir(parents=True, exist_ok=True)


    with open(log_read_path, "w") as log_file:
        sys.stdout = log_file

        #--Crea instancia con la aplicacion
        outlook = win32com.client.Dispatch('Outlook.Application')


        #--Se designa cuenta a consultar y tipo de archivos a descargar
        namespace = outlook.GetNamespace('MAPI')
        accounts = namespace.Accounts
        desired_account = None

        #--Itera sobre las cuentas
        for account in accounts:
            if account_name in account.DisplayName:
                desired_account = account
                break

        #--Dentro de la cuenta encontrada se para sobre la carpeta definida
        if desired_account is not None:
            inbox = desired_account.DeliveryStore.GetDefaultFolder(6)

            subfolder_name = 'Respaldo xml'
            subfolder = inbox.Folders[subfolder_name]

            messages = subfolder.Items

            #--Definimos el filtro de fecha a consultar
            restriction = f"[ReceivedTime] >= '{date_from_download.strftime('%d/%m/%Y %H:%M')}' AND [ReceivedTime] < '{date_until_download.strftime('%d/%m/%Y %H:%M')}'"
            filtered_messages = messages.Restrict(restriction)

            #--Iteramos sobre los mensajes
            for message in filtered_messages:
                if message.Subject:
                    attachments = message.Attachments
                    for attachment in attachments:
                        if attachment.FileName.lower().endswith(file_format):
                            if not os.path.exists(output_folder):
                                os.makedirs(output_folder)
                            try:
                                doc = DocXml.objects.get(sobre = attachment)
                                print(f'{doc} Objeto ya creado {attachment}')
                                pass

                            except DocXml.DoesNotExist:
                                if not re.search(r'^(M|ME|Rech)_', attachment.FileName):
                                   attachment.SaveAsFile(os.path.join(output_path, attachment.FileName))
                            
                            except Exception as e:
                                print(f'Error en el proceso {message.Subject} {str(e)}')

                            print(f'{attachment}\n')

            print(f'Archivos adjuntos descargados del {date_until_download}')
        return outlook
    
def main():
    outlook_instance = SaveMail()
    ProcessXml()

    sys.stdout = sys.__stdout__
    print('Proceso completo')

if __name__ == "__main__":
    main()