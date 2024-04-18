from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app.views import get_main_page, get_user_page

app_name = 'app'

urlpatterns = [
    path('', get_main_page, name='main'),
    path('<int:pk>/', get_user_page, name='personal'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
