from django.http import HttpResponse
from django.shortcuts import render
from .models import Connection,Source
from api.services.crypt import cipher_suite

def index(request):
    # decrypt password
    obj = Connection.objects.first()
    try:
        cipher_suite().decrypt(obj.password.encode())
    except Exception as e:
        print("eeeeeee********************************", e)
    return HttpResponse('hello')