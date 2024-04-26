
import locale
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import ReportForm
from app.models import Report, User


@login_required
def get_main_page(request):
    if request.user.role.slug != 'administrator':
        return redirect(
            reverse('app:personal', kwargs={'pk': request.user.pk})
        )
    dates = [
        date[0] for date
        in Report.objects.values_list('date').order_by('-date').distinct()
    ]
    reports = Report.objects.filter(date=dates[0])
    context = {'reports': reports}
    if len(dates) > 1:
        context.update({'next': dates[1]})
    return render(request, 'main.html', context)


@login_required
def get_daily_reports_page(request, date):
    if request.user.role.slug == 'administrator':
        dates = [
            str(date[0]) for date
            in Report.objects.values_list('date').order_by('-date').distinct()
        ]
        date_index = dates.index(date)
        reports = Report.objects.filter(date=date)
        context = {'reports': reports}
        if len(dates) > 1:
            if date_index < len(dates) - 1:
                context.update({'next': dates[date_index + 1]})
            if date_index == 1:
                context.update({'prev': reverse('app:main')})
            context.update({'prev': dates[date_index - 1]})
        return render(request, 'daily_reports.html', context)


@login_required
def get_manager_page(request, pk):
    if (
        request.user.pk == pk
        or request.user.role.slug == 'administrator'
        and pk != 1
    ):
        if request.user.pk == pk and request.user.role.slug == 'administrator':
            return redirect(reverse('app:main'))
        reports = Report.objects.filter(manager=pk).order_by('-date')
        manager = User.objects.get(pk=pk)
        context = {
            'reports': reports,
            'manager': manager
        }
        return render(request, 'personal.html', context)
    return render(request, '404.html', {'users': request.user})


@login_required
def create_report(request):
    if request.user.role.slug == 'administrator':
        return redirect(reverse('app:main'))
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            manager = request.user
            address = form.cleaned_data['address']
            date = datetime.now()
            income = form.cleaned_data['income']
            Report.objects.get_or_create(
                manager=manager,
                address=address,
                date=date,
                income=income
            )
            return redirect(
                reverse('app:personal', kwargs={'pk': request.user.pk})
            )
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form})


@login_required
def edit_report(request, pk):
    report = Report.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report.address = form.cleaned_data['address']
            report.income = form.cleaned_data['income']
            report.save()
            return redirect(
                reverse('app:personal', kwargs={'pk': request.user.pk})
            )
    else:
        data = {
            'date': report.date,
            'income': report.income
        }
        form = ReportForm(initial=data)
    return render(request, 'report.html', {'form': form})


@login_required
def get_monthly_reports(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    total_income = (
        Report.objects.annotate(
            month=ExtractMonth('date')
        ).values(
            'month'
        ).annotate(
            year=ExtractYear('date')
        ).annotate(
            total=Sum('income')
        )
    )
    for i in total_income:
        month_number = i['month']
        i['month'] = datetime(1990, month_number, 1).strftime('%B')
    return render(request, 'monthly.html', {'total_income': total_income})
