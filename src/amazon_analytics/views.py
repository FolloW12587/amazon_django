from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
import json

from . import forms, reports, models


@login_required
def upload(request):
    if request.method == 'POST':
        form = forms.UploadReportFrom(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            return reports.handle_uploaded_file(cd['report_file'], cd['name'], cd['period_date'], request.user)
    else:
        form = forms.UploadReportFrom()
    return render(request, 'amazon_analytics/upload.html', {'form': form})


@login_required
def index(request):
    if request.method == 'POST':
        form = forms.GetReportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            report = reports.get_report(cd['period_date_start'], cd['period_date_end'], cd['limit'])
            return report
    else:
        form = forms.GetReportForm()
    date_limits = json.dumps(list(models.Reports.objects.values_list('period_date', flat=True).distinct().order_by('-period_date')), cls=DjangoJSONEncoder)
    return render(request, 'amazon_analytics/get_report_form.html', {'form': form, 'date_limits': date_limits})

