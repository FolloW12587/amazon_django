from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from amazon_analytics import models


@admin.register(models.Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'period_date', 'uploaded_by', 'uploaded_date')
    date_hierarchy = 'period_date'

    search_fields = ('id', 'name', 'period_date', 'uploaded_by')
    list_filter = (('uploaded_by', RelatedDropdownFilter),)


@admin.register(models.Requests)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'request')

    search_fields = ('id', 'request')


@admin.register(models.RequestTops)
class RequestTopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'report', 'position')

    search_fields = ('id', 'request', 'report')
    list_filter = (('report', RelatedDropdownFilter),)
