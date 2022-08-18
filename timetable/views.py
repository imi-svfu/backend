from django.contrib import admin
from django.shortcuts import render


def index_page(request):
    context = {
    } | dict(admin.site.each_context(request))
    return render(request, 'timetable/index.html', context)
