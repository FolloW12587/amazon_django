from django.urls import path

from amazon_analytics import views


urlpatterns = [
    path('', views.index),
    path('upload', views.upload),
]