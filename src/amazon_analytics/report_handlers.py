from django.conf import settings

import os


def handle_uploaded_file(f, name):
    full_path = os.path.join(settings.BASE_DIR, r'amazon_analytics/static/amazon_analytics/reports', name)
    with open(full_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
        
