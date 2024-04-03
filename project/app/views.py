from django.shortcuts import render
from .models import User


def get_main_page(request):
    users = User.objects.all()
    return render(request, 'main.html', {'users': users})
