import sys
import os
import django
from variables import project_directory, destination_account

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

#--------------------------------------------------------------#

sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReadXml.settings")
django.setup()

from Model.models import *
#--------------------------------------------------------------#

def send_mail_finan_fact(excel_path_item, excel_path_fact, date_download):
    subject = f"Documentos para subir - {date_download}"
    message = render_to_string('mail.html', {
        'nameFact': excel_path_fact,
        'fecha': date_download,
        'nameFact2': excel_path_item,
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
              destination_account)
    email.attach_file(excel_path_fact)
    email.attach_file(excel_path_item)
    email.send()

def send_mail_finan_ret17453(excel_path_item, excel_path_fact, date_download):
    subject = f"Documentos para subir - {date_download}"
    message = render_to_string('mail.html', {
        'nameFact': excel_path_fact,
        'fecha': date_download,
        'nameFact2': excel_path_item,
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
              destination_account)
    email.attach_file(excel_path_fact)
    email.attach_file(excel_path_item)
    email.send()

def send_mail_finan_ret18910(excel_path_item, excel_path_fact, date_download):
    subject = f"Documentos para subir - {date_download}"
    message = render_to_string('mail.html', {
        'nameFact': excel_path_fact,
        'fecha': date_download,
        'nameFact2': excel_path_item,
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
              destination_account)
    email.attach_file(excel_path_fact)
    email.attach_file(excel_path_item)
    email.send()

def send_mail_finan_ret19210(excel_path_item, excel_path_fact, date_download):
    subject = f"Documentos para subir - {date_download}"
    message = render_to_string('mail.html', {
        'nameFact': excel_path_fact,
        'fecha': date_download,
        'nameFact2': excel_path_item,
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
              destination_account)
    email.attach_file(excel_path_fact)
    email.attach_file(excel_path_item)
    email.send()

