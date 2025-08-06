from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import CharField, DecimalField, F, Sum, Value
from django.db.models.functions import Cast, Concat, ExtractMonth, ExtractYear
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import ReportForm
from app.models import Report, User

# Страницы для админа


@login_required
def main_page(request):
    """Главная страница."""

    if request.user.role.slug == 'admin':
        managers = User.objects.filter(role__slug='manager')
        return render(request, 'main_page.html', {'managers': managers})

    return redirect(reverse('app:personal', kwargs={'pk': request.user.pk}))


@login_required
def daily_reports(request, date):
    """Страницы ежедневных отчётов."""

    if request.user.role.slug == 'admin':
        dates = [
            str(date[0]) for date
            in Report.objects.values_list('date').order_by('-date').distinct()
        ]
        reports = Report.objects.filter(date=date)
        context = {'reports': reports, 'dates': dates, 'current_date': date}
        return render(request, 'daily_reports.html', context)

    return render(request, '404.html')


@login_required
def monthly_reports(request):
    """Общая страница сводных отчётов."""

    if request.user.role.slug == 'admin':
        month_income = (
            Report.objects
            .annotate(month=ExtractMonth('date'))
            .values('month')
            .annotate(year=ExtractYear('date'))
            .annotate(total=Cast(Sum('income'), output_field=DecimalField()))
            .annotate(
                detail=(
                    Concat(
                        F('month'),
                        Value('-'),
                        F('year'),
                        output_field=CharField()
                    )
                )
            )
        )
        return render(
            request, 'monthly_reports.html', {'month_income': month_income}
        )

    return render(request, '404.html', {'users': request.user})


@login_required
def monthly_detail(request, month):
    """Страница детализации отчётности за выбранный месяц."""

    if request.user.role.slug == 'admin':
        month_year = month.split('-')
        reports = (
            Report.objects.filter(
                date__year=month_year[1],
                date__month=month_year[0]
            )
        )
        return render(request, 'monthly_detail.html', {'reports': reports})

    return render(request, '404.html', {'users': request.user})


# Страницы для менеджера


@login_required
def get_manager_page(request, pk):
    """Персональная страница менеджера."""

    if (
        request.user.pk == pk
        or request.user.role.slug == 'admin'
        and pk != 1
    ):
        if request.user.pk == pk and request.user.role.slug == 'admin':
            return redirect(reverse('app:main_page'))

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
        return redirect(reverse('app:main_page'))

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
            report.date = form.cleaned_data['date']
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


@login_required
def delete_report(request, pk):
    report = Report.objects.get(pk=pk)
    report.delete()
    return redirect(reverse('app:personal', kwargs={'pk': request.user.pk}))


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


def page_not_found(request, exception):
    return render(request, '404.html', {'path': request.path}, status=404)
