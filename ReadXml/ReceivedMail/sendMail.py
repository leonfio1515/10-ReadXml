import sys
import os
import django
from variables import project_directory,adressee_finan, adressee_prov

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from datetime import timedelta
#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#


def send_mail_finan(excel_path_item, excel_path_fact, date_process,document_type):
    subject = f"Documentos para subir {document_type} - {date_process}"
    message = render_to_string('mail_finan.html', {
        'nameFact': excel_path_fact,
        'fecha': date_process,
        'hasta':date_process - timedelta(days=1),
        'nameFact2': excel_path_item,
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
              adressee_finan)
    email.attach_file(excel_path_fact)
    email.attach_file(excel_path_item)
    email.send()


def send_mail_prov_fact(excel_path_item, excel_path_fact, date_process, document_type):
    subject = f"Documentos para subir {document_type} - {date_process}"
    message = render_to_string('mail_prov.html', {
        'nameFact': excel_path_fact,
        'fecha': date_process,
        'hasta':date_process - timedelta(days=1),
        'nameFact2': excel_path_item,
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
              adressee_prov)
    email.attach_file(excel_path_fact)
    email.attach_file(excel_path_item)
    email.send()