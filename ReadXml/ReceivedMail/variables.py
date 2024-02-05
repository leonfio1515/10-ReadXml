from datetime import date, timedelta
import os
from pathlib import Path

#----------------DIRECTORIO DJANGO--------------------------#

today = date.today()


#Se crea instancia del directorio para definir las rutas de los archivos.
project_directory = os.path.dirname(os.path.abspath(__file__))  
project_directory = os.path.dirname(project_directory)

#-------------------Dates---------------------------#
#Se definen las fechas con las que se van a trabajar

date_until_download = today #Fecha del dia de hoy
date_from_download = today - timedelta(days=15) #Fecha de los documentos a descargar
date_process = today - timedelta(days=0) #Fecha de los documentos a procesar. El procesose ejecuta segun la fecha de creacion de los mismos.


#---------------Outlook Accound-------------------------#

#Definir account_name con la cuenta de outlook de la que extraera los XML
account_name = 'youOutlookAcount@example.com'
subfolder_name = 'Name folder'

file_format = '.xml'

#Definir la cuenta/s a la/s que se enviaran los correos de confirmacion.
destination_account = ['sendMail@example.com']


#---------------Download Files-------------------------#
rute_path = project_directory


output_folder = Path(rute_path) / "ReceivedMail" / f'Mail recibidos 2023-09-23'
output_path = os.path.join( rute_path , f'ReceivedMail\Mail recibidos 2023-09-23')

log_console = f'z.Mail recibidos-Logs {date_until_download}'
log_path = os.path.join(output_folder, log_console)

log_read = f'z.Logs proceso Read {date_until_download}'
log_read_path = os.path.join(output_folder, log_read)

log_readfail = f'z.Logs proceso ReadFail {date_until_download}'
log_readfail_path = os.path.join(output_folder, log_readfail)


log_df_prov = f'z.Logs proceso DataFrame Proveedores {date_until_download}'
log_df_prov_path = os.path.join(output_folder, log_df_prov)

log_df_finan_fact = f'z.Logs proceso DataFrame Financieras Fact {date_until_download}'
log_df_finan_fact_path = os.path.join(output_folder, log_df_finan_fact)

log_df_finan_resg = f'z.Logs proceso DataFrame Financieras Resg {date_until_download}'
log_df_finan_resg_path = os.path.join(output_folder, log_df_finan_resg)

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

tax_map = {
    '0':'IVA CEXE',
    '22':'IVA CTB',
    '10':'IVA CTM',
}

norma_financieras = {
    '3239 - cupones':'G_191',
    '3239 - ordenes':'G_214',
    '13338501':'G_163',
    '31207 - cupones':'G_71',
    '64400 - cupones':'G_75',
    '11020401':'G_162',
    '11020413':'G_71',
    '13338501':'G_163',
    '13338503':'G_71',
    '13338504':'G_163',
    '13881101':'G_75',
    '5722':'G_143',
    '378282':'G_144',
    '501444':'G_75',
    '297469':'G_71',
    '505914':'G_77',
    '000265129396':'G_71',
    '000747437617':'G_75',
    '000452961396':'G_71',
}

#------------------DATA FRAME FACT VARIABLES----------------------#
prov_num_fact_var_finan = []
doc_num_fact_var_finan = []
doc_date_fact_var_finan = []
doc_date_exp_fact_var_finan = []
control_accoun_var_finan = []
currency_fact_var_finan = []
doc_num_item_fact_var_finan = []
desc_item_fact_var_finan = []
item_num_fact_var_finan = []
article_fact_var_finan = []
amount_fact_var_finan = []
amount_item_fact_var_finan = []
norm_fact_var_finan = []
norm_f_fact_var_finan = []
memo_fact_var_finan = []
tax_type_fact_var_finan = []
currency_item_fact_var_finan = []
quantity_fact_var_finan = []
wHouse_fact_var_finan = []
date_from_fact_var_finan = []
date_until_fact_var_finan = []
free_text_fact_var_finan = []

#------------------DATA FRAME FACT VARIABLES----------------------#
prov_num_fact_var = []
doc_num_fact_var = []
doc_date_fact_var = []
doc_date_exp_fact_var = []
control_accoun_var = []
currency_fact_var = []
doc_num_item_fact_var = []
desc_item_fact_var = []
item_num_fact_var = []
article_fact_var = []
amount_fact_var = []
amount_item_fact_var = []
norm_fact_var = []
norm_f_fact_var = []
memo_fact_var = []
tax_type_fact_var = []
currency_item_fact_var = []
quantity_fact_var = []
wHouse_fact_var = []
date_from_fact_var = []
date_until_fact_var = []
free_text_fact_var = []