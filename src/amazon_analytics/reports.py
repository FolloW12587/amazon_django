import csv
import datetime
import os

from . import models
from django.conf import settings
from django.db import connection
from django.http import HttpResponse


def handle_uploaded_file(f, name):
    full_path = os.path.join(settings.BASE_DIR, r'amazon_analytics/static/amazon_analytics/reports', name)
    with open(full_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
        

def get_report(date_from, date_to, limit):
    sql_file = os.path.join(settings.BASE_DIR, r'amazon_analytics/sql/request_v1.sql')
    if not os.path.exists(sql_file):
        return HttpResponse("Error! Can't find sql request")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Запрос', date_from, date_to, "Изменение позиции", "Абсолютное изменение позиции"])
    
    with connection.cursor() as cursor:
        with open(sql_file, 'r') as r:
            cursor.execute(r.read(), [date_from, date_to, limit])
        while True:
            row = cursor.fetchone()
            if not row:
                break
            writer.writerow(row)

    return response