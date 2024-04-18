from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import User


@login_required
def get_main_page(request):
    managers = User.objects.filter(is_superuser=False)
    return render(request, 'main.html', {'managers': managers})


@login_required
def get_user_page(request, pk):
    if request.user.pk == pk or request.user.is_superuser:
        return render(request, 'personal.html', {'user': request.user})
    else:
        return render(request, '404.html', {'users': request.user})
