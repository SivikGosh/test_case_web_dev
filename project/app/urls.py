from django.contrib.auth.views import LogoutView
from django.urls import path

from app.views import (
    CustomLoginView,
    create_report,
    daily_reports,
    delete_report,
    edit_report,
    get_manager_page,
    main_page,
    monthly_detail,
    monthly_reports,
)

app_name = 'app'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('daily/<slug:date>/', daily_reports, name='daily_reports'),
    path('monthly/', monthly_reports, name='monthly_reports'),
    path('monthly/<slug:month>/', monthly_detail, name='monthly_detail'),
    path('managers/<int:pk>/', get_manager_page, name='personal'),
    path('report/', create_report, name='report'),
    path('report/<int:pk>/edit/', edit_report, name='edit_report'),
    path('report/<int:pk>/delete/', delete_report, name='delete_report'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
