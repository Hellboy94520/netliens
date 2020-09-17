from django.shortcuts import render, redirect


def home(request):
    # GET
    return render(request, 'home.html')