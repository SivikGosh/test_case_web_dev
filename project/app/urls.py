from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app.views import (
    create_report,
    edit_report,
    get_daily_reports,
    get_main_page,
    get_manager_page,
    get_monthly_reports,
    get_monthly_detail_report,
    CustomLoginView
)

app_name = 'app'

urlpatterns = [
    path(
        '',
        get_main_page,
        name='main'
    ),
    path(
        'managers/<int:pk>/',
        get_manager_page,
        name='personal'
    ),
    path(
        'monthly/',
        get_monthly_reports,
        name='monthly'
    ),
    path(
        'monthly/<slug:month>/',
        get_monthly_detail_report,
        name='monthly_detail'
    ),
    path(
        'daily/<slug:date>/',
        get_daily_reports,
        name='daily_reports'
    ),
    path(
        'report/',
        create_report,
        name='report'),
    path(
        'report/<int:pk>/edit/',
        edit_report,
        name='edit_report'
    ),
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]
