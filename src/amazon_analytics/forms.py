from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from . import models, mixins

import datetime


class UploadReportFrom(forms.Form, mixins.WeekdayFinderMixin):
    name = forms.CharField(label='Название отчета', max_length=255)
    period_date = forms.DateField(label='Дата отчетного периода', widget=AdminDateWidget)
    report_file = forms.FileField(label='Файл с данными')

    def __init__(self, *args, **kwargs):
        super(UploadReportFrom, self).__init__(*args, **kwargs)
        self.fields['period_date'].initial = self.get_saturday
        self.fields['period_date'].widget.attrs['readonly'] = True

    def clean_period_date(self):
        period_date = self.cleaned_data['period_date']
        if models.Reports.objects.filter(period_date=period_date):
            raise ValidationError('Data for this period is already in database!')
        if not self.check_weekday(6, period_date):
            raise ValidationError('The weekday for uploaded report must be saturday!')
        return period_date

    def clean_name(self):
        name = self.cleaned_data['name']
        if models.Reports.objects.filter(name=name).count() > 0:
            raise ValidationError('File with such name is already in database!')
        return name


class GetReportForm(forms.Form, mixins.WeekdayFinderMixin):
    period_date_start = forms.DateField(label='Начало периода для отчета', widget=AdminDateWidget)
    period_date_end = forms.DateField(label='Конец периода для отчета', widget=AdminDateWidget)
    limit = forms.IntegerField(label="Количество строк в отчете", initial=100, min_value=0, max_value=1000000)
    
    def __init__(self, *args, **kwargs):
        super(GetReportForm, self).__init__(*args, **kwargs)
        self.fields['period_date_start'].initial = (models.Reports.objects.order_by('-period_date').first().period_date \
            if models.Reports.objects.order_by('-period_date').first() != None else self.get_saturday)
        self.fields['period_date_start'].widget.attrs['readonly'] = True
        
        self.fields['period_date_end'].initial = (models.Reports.objects.order_by('-period_date').first().period_date \
            if models.Reports.objects.order_by('-period_date').first() != None else self.get_saturday)
        self.fields['period_date_end'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['period_date_start'] > cleaned_data['period_date_end']:
            raise ValidationError('Start date must be less or equal to end date')

