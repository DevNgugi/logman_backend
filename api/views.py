from django.shortcuts import render

# Create your views here.
def index(request, socket_id):
    return render(request, "index.html")