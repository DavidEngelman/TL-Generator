import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, render_to_response
from django.urls import path, reverse

from django.core.checks import messages
from timelinesGenerator.parser import FileManager


def index(request):
    return render(request, 'timelines.html')


def upload_file(request):
    try:
        file = request.FILES["file"]
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'File is not xlsx type')
            return HttpResponseRedirect(reverse("index"))
        # if file is too large, return
        if file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("index"))

        data = FileManager.parse(file)

        print(data, type(data))

        return render(request, 'timelines.html', {'JSON_data': data})



    except Exception as e:
        messages.error(request, "Unable to upload file. " + repr(e))
