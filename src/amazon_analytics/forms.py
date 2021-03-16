from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from . import models 

import datetime


class UploadReportFrom(forms.Form):
    name = forms.CharField(label='Название отчета', max_length=255)
    period_date = forms.DateField(label='Дата отчетного периода', initial=datetime.date.today, widget=AdminDateWidget)
    report_file = forms.FileField(label='Файл с данными')

    def clean_period_date(self):
        period_date = self.cleaned_data['period_date']
        if models.Reports.objects.filter(period_date=period_date):
            raise ValidationError('Data for this period is already in database')
        return period_date

    def clean_name(self):
        name = self.cleaned_data['name']
        if models.Reports.objects.filter(name=name).count() > 0:
            raise ValidationError('File with such name is already in database')

        return name


class GetReportForm(forms.Form):
    period_date_start = forms.DateField(label='Начало периода для отчета', \
        initial=(models.Reports.objects.order_by('-period_date').first().period_date if models.Reports.objects.order_by('-period_date').first() != None else datetime.date.today), widget=AdminDateWidget)
    period_date_end = forms.DateField(label='Конец периода для отчета', \
        initial=(models.Reports.objects.order_by('-period_date').first().period_date  if models.Reports.objects.order_by('-period_date').first() != None else datetime.date.today), widget=AdminDateWidget)
    limit = forms.IntegerField(label="Количество строк в отчете", initial=100, min_value=10, max_value=10000)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['period_date_start'] > cleaned_data['period_date_end']:
            raise ValidationError('Start date must be less or equal to end date')

