from celery import shared_task
from time import sleep
from . models import *
import pandas
from django.core.mail import EmailMessage, send_mail
import io
from django.core.exceptions import ValidationError

def str_to_bool(value):
    if value.lower() in ('true', '1'):
        return True
    elif value.lower() in ('false', '0'):
        return False
    raise ValidationError(f'Invalid boolean value: {value}')


@shared_task
def sendMailTask(enrollee_data_list):
    df_export = pandas.DataFrame(enrollee_data_list)

    output = io.BytesIO()
    df_export.to_excel(output, index=False, engine='openpyxl')
    output.seek(0) 

    try:
        email = EmailMessage(
            subject='Filtered Enrollee Data',
            body='Please find the attached Excel file with the filtered enrollee data.', 
            from_email='ujjwal@gftpl.in', 
            to=['ujjwal@gftpl.in'], 
        )

        email.attach('filtered_enrollee_data.xlsx', output.getvalue(),
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.send(fail_silently=False)
    except Exception as e:
        print(f"{e = }")
    return None
