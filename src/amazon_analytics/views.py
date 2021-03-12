from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def upload(request):
    return HttpResponse("Hello, world! This is a page for upload form.")


@login_required
def index(request):
    return HttpResponse("Hello, world! This is a page for download report form.")