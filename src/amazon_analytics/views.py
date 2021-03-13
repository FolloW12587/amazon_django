from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from . import forms, report_handlers


@login_required
def upload(request):
    if request.method == 'POST':
        form = forms.GetReportFrom(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            report_handlers.handle_uploaded_file(cd['report_file'], cd['name'])
            return HttpResponse(str(cd))
    else:
        form = forms.GetReportFrom()
    return render(request, 'amazon_analytics/upload.html', {'form': form})


@login_required
def index(request):
    return HttpResponse("Hello, {user}! This is a page for download report form.".format(user=request.user))

