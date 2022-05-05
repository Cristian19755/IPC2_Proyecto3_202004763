from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def inicio(request):
    return render(request, 'pPlantilla.html')