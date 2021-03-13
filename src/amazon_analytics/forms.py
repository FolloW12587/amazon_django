from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from . import models 

import datetime


class GetReportFrom(forms.Form):
    name = forms.CharField(label='Название отчета', max_length=255)
    period_date = forms.DateField(label='Дата отчетного периода', initial=datetime.date.today, widget=AdminDateWidget)
    report_file = forms.FileField(label='Файл с данными')

    def clean_name(self):
        name = self.cleaned_data['name']
        if models.Reports.objects.filter(name=name).count() > 0:
            raise ValidationError('File with such name is already in database')

        return name