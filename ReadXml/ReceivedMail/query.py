import sys
import os
import django
from variables import project_directory, date_process

#-----------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#

factsFinan = DocXml.objects.filter(doc_type=111, date_create = date_process, rut__prov_type='Financiera')
resgsFinan = DocXml.objects.filter(doc_type=182, date_create = date_process, rut__prov_type='Financiera')

factsProv = DocXml.objects.filter(doc_type=111, date_create = date_process, rut__prov_type='Proveedor')
resgsProv = DocXml.objects.filter(doc_type=182, date_create = date_process, rut__prov_type='Proveedor')

factsUte = DocXml.objects.filter(doc_type=111, date_create = date_process, rut__rut=210778720012)

