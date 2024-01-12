from django.shortcuts import render

#import HttpResponse object from the django.http module
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there partner!")
