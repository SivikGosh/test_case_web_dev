from django.shortcuts import render
from .models import User


def test(request):
    users = User.objects.all()
    return render(request, 'base.html', {'users': users})