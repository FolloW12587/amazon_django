import csv
import datetime
import os

from . import models
from django.conf import settings
from django.db import connection
from django.http import HttpResponse


def handle_uploaded_file(f, name, period_date, user):
    full_path = os.path.join(settings.BASE_DIR, r'amazon_analytics/static/amazon_analytics/reports', name)

    decoded_file = f.read().decode('utf-8').splitlines()[1:-1]
    reader = csv.DictReader(decoded_file)
    report = models.Reports(period_date=period_date, name=name, uploaded_by=user)
    report.save()

    with open(full_path, 'w') as wr:
        wr.write('Search Term,Search Frequency Rank,Report id,User id\n')
        for row in reader:
            request = row['Search Term']
            if len(request) > 255:
                continue
            top = row['Search Frequency Rank'].replace(',', '')
            new_row = '","'.join(['"'+request, top, str(report.pk), str(user.pk) + '"'])
            wr.write(new_row+'\n')
    
    models.TemporaryRequestTops.objects.from_csv(full_path, dict(request="Search Term", position="Search Frequency Rank", report_id="Report id", user_id="User id"))
    with connection.cursor() as cursor:
        sql_upload_requests_file = os.path.join(settings.BASE_DIR, r'amazon_analytics/sql/upload_missing_requests.sql')
        sql_upload_tops_file = os.path.join(settings.BASE_DIR, r'amazon_analytics/sql/upload_tops.sql')
        if not os.path.exists(sql_upload_requests_file) or not os.path.exists(sql_upload_tops_file):
            models.TemporaryRequestTops.objects.filter(user_id=user.pk).delete()
            return HttpResponse("Error! Can't find sql requests")

        with open(sql_upload_requests_file) as r:
            cursor.execute(r.read())

        with open(sql_upload_tops_file) as r:
            cursor.execute(r.read())

    models.TemporaryRequestTops.objects.filter(user_id=user.pk).delete()
    os.remove(full_path)
    return HttpResponse('success')        
        

def get_report(date_from, date_to, limit):
    sql_file = os.path.join(settings.BASE_DIR, r'amazon_analytics/sql/request_v2.sql')
    if not os.path.exists(sql_file):
        return HttpResponse("Error! Can't find sql request")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Запрос', date_from, date_to, "Минимальная позиция", "Максимальная позиция",\
        "Разница между мин и макс", "Изменение позиции", "Абсолютное изменение позиции"])

    params_list = [date_from, date_to]*3
    with connection.cursor() as cursor:
        with open(sql_file, 'r') as r:
            if limit == 0:
                limit_str = 'ALL'
            else:
                limit_str = r'%s'
                params_list.append(limit)
            cursor.execute(r.read().format(limit=limit_str), params_list)
        while True:
            row = cursor.fetchone()
            if not row:
                break
            writer.writerow(row)

    return response