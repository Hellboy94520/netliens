from django.shortcuts import render, redirect
from ..models import User

def home(request):
    # GET
    return render(request, 'home.html')