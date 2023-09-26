from datetime import date, timedelta
import os
from pathlib import Path

#----------------DIRECTORIO DJANGO--------------------------#
#Se crea instancia del directorio para definir las rutas de los archivos.
project_directory = os.path.dirname(os.path.abspath(__file__))  
project_directory = os.path.dirname(project_directory)

#-------------------Dates---------------------------#
#Se definen las fechas con las que se van a trabajar

today = date.today() #Fecha del dia de hoy
date_download = today - timedelta(days=2) #Fecha de los documentos a descargar
date_process = today #Fecha de los documentos a procesar. El procesose ejecuta segun la fecha de creacion de los mismos.


#---------------Outlook Accound-------------------------#

#Definir account_name con la cuenta de outlook de la que extraera los XML
account_name = 'youOutlookAcount@example.com'
subfolder_name = 'Name folder'

file_format = '.xml'

#Definir la cuenta/s a la/s que se enviaran los correos de confirmacion.
destination_account = ['sendMail@example.com']


#---------------Download Files-------------------------#

#Se crean las rutas y los nombres de los archivos a consultar y guardar.
output = Path(project_directory) / "ReceivedMail" / f'Mail recibidos {date_download}'
salida = os.path.join( project_directory , f'ReceivedMail\Mail recibidos {date_download}')

folder_path = Path(project_directory) /  "ReceivedMail" / f'Mail recibidos {date_download}'
log_console = f'z.Mail recibidos-Logs {date_download}'


#--------------------------------------------#
#Variables constantes.
#Se determinan casos constantes para realizar filtrados dentro de las query y la asignacion de valores.
cost_envio = 'Descuento Envio Liq. y Cheque'
cost_cod = 'GTO000804'

retencion = '2183161'
ret_cod = 'GTO000044'

financiacion = 'FINANCIACION'
finan_cod = 'GTO000814'

ticket = 'Ticket Compliments® Electrónico'


#------------------DATA FRAME FACT----------------------#
#Se definen las listas con las que se generaran los DataFrame
prov_num = []
doc_num_fact = []
doc_date = []

doc_num_item = []
item_num = []
article = []
amount = []

#------------------DATA FRAME RESG----------------------#
doc_num_resg17453 = []
doc_date_resg17453 = []
account_prov_resg17453 = []
amount_resg17453 = []

doc_num_resg19210 = []
doc_date_resg19210 = []
account_prov_resg19210 = []
amount_resg19210 = []

doc_num_resg18910 = []
doc_date_resg18910 = []
account_prov_resg18910 = []
amount_resg18910 = []

doc_num_item_resg = []
item_num_resg = []

item_17453 = []
item_19210 = []
item_18910 = []


