
import locale
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import CharField, F, Sum, Value
from django.db.models.functions import Concat, ExtractMonth, ExtractYear
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import ReportForm
from app.models import Report, User


@login_required
def get_main_page(request):
    """Главная страница. Она же первая страница ежедневных отчётов."""

    if request.user.role.slug != 'admin':
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
def get_daily_reports(request, date):
    """Страницы едежневных отчётов, все, кроме первой."""

    if request.user.role.slug != 'admin':
        return render(request, '404.html', {'users': request.user})

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
def get_monthly_reports(request):
    """Общая страница сводных отчётов."""

    if request.user.role.slug != 'admin':
        return render(request, '404.html', {'users': request.user})

    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    month_income = (
        Report.objects
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(year=ExtractYear('date'))
        .annotate(total=Sum('income'))
        .annotate(
            detail=Concat(
                F('month'), Value('-'), F('year'), output_field=CharField()
            )
        )
    )

    for income in month_income:
        month_number = income['month']
        income['month'] = datetime(1990, month_number, 1).strftime('%B')

    return render(request, 'monthly.html', {'month_income': month_income})


@login_required
def get_monthly_detail_report(request, month):
    """Страница детализации отчётности за выбранный месяц."""

    if request.user.role.slug != 'admin':
        return render(request, '404.html', {'users': request.user})

    month_year = month.split('-')

    reports = Report.objects.filter(
        date__year=month_year[1], date__month=month_year[0]
    )

    return render(request, 'monthly_reports.html', {'reports': reports})


@login_required
def get_manager_page(request, pk):
    """Персональная страница менеджера."""

    if (
        request.user.pk == pk
        or request.user.role.slug == 'admin'
        and pk != 1
    ):
        if request.user.pk == pk and request.user.role.slug == 'admin':
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
    """Страница добавления отчёта."""

    if request.user.role.slug == 'admin':
        return redirect(reverse('app:main'))

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            manager = request.user
            address = form.cleaned_data['address']
            date = form.cleaned_data['date']
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
        form = ReportForm(initial={'date': datetime.now()})
    return render(request, 'report.html', {'form': form})


@login_required
def edit_report(request, pk):
    """Страница редактирования отчёта."""

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
            'address': report.address,
            'date': report.date,
            'income': report.income
        }
        form = ReportForm(initial=data)
    return render(request, 'report.html', {'form': form})


class CustomLoginView(LoginView):
    """Авторизация."""

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request,
            'Неправильно введён логин и/или пароль, \
                или такого пользователя не существует.'
        )
        return response
