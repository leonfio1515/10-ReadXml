import os
import win32com.client

from variables import *
from processXml import ProcessXml
#--------------------------------------------------------------#

#-- LEE LOS MAIL Y DESCARGA LOS XML --#

#--Crea directorio para guardar los mail descargados
output.mkdir(parents=True, exist_ok=True)


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
    subfolder = inbox.Folders[subfolder_name]
    messages = subfolder.Items

    #--Definimos el filtro de fecha a consultar
    restriction = f"[ReceivedTime] >= '{date_download.strftime('%m/%d/%Y %H:%M %p')}'"
    filtered_messages = messages.Restrict(restriction)

    #--Iteramos sobre los mensajes
    for message in filtered_messages:
        if message.Subject:
            attachments = message.Attachments
            for attachment in attachments:
                if attachment.FileName.lower().endswith(file_format):
                    if not os.path.exists(output):
                        os.makedirs(output)
                    attachment.SaveAsFile(os.path.join(salida, attachment.FileName))

    print(f'Archivos adjuntos descargados del {date_download}')
else:
    print('Cuenta no encontrada en el correo')

# ProcessXml()
