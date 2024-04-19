from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app.views import (
    create_report, edit_report, get_main_page, get_manager_page
)

app_name = 'app'

urlpatterns = [
    path('', get_main_page, name='main'),
    path('<int:pk>/', get_manager_page, name='personal'),
    path('report/', create_report, name='report'),
    path('<int:pk>/edit/', edit_report, name='edit_report'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
