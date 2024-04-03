from django.urls import path
from .views import get_main_page

urlpatterns = [
    path('', get_main_page, name='main')
]
