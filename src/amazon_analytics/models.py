from django.conf import settings
from django.db import models
from postgres_copy import CopyManager


class Reports(models.Model):
    id = models.AutoField("id", primary_key=True)
    period_date = models.DateField("Дата отчетного периода", unique=True)
    name = models.CharField("Название отчета", blank=True, null=True, max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Загружено пользователем', on_delete=models.CASCADE)
    uploaded_date = models.DateTimeField("Дата загрузки", auto_now_add=True)

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return '{}'.format(self.name)


class Requests(models.Model):
    id = models.AutoField("id", primary_key=True)
    request = models.CharField('Запрос', max_length=255)

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"

    def __str__(self):
        return '{}'.format(self.request)


class RequestTops(models.Model):
    id = models.AutoField("id", primary_key=True)
    request = models.ForeignKey(Requests, on_delete=models.CASCADE, verbose_name="Запрос")
    report = models.ForeignKey(Reports, on_delete=models.CASCADE, verbose_name="Отчет")
    position = models.IntegerField('Позиция запроса')

    class Meta:
        verbose_name = "Позиция запроса"
        verbose_name_plural = "Позиции запросов"
        
    def __str__(self):
        return '[{pos}] {req}'.format(pos=self.position, req=self.request.request)


class TemporaryRequestTops(models.Model):
    id = models.AutoField("id", primary_key=True)
    request = models.CharField('Запрос', max_length=255)
    position = models.IntegerField('Позиция запроса')
    report_id = models.IntegerField('ID отчета')

    objects = CopyManager()