from django.shortcuts import render


def home(request):
    return render(request, 'provision/home.html')
