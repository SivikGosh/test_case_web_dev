from datetime import datetime
# from app.models import Report


def current_month(request):
    return {'current_month': datetime.now().month}


# def newest_date_reports(request):
#     dates = [
#         str(date[0]) for date
#         in Report.objects.values_list('date').order_by('-date').distinct()
#     ]
#     try:
#         return {'newest_date': dates[0]}
#     except IndexError:
#         return {'newest_date': datetime.now().date}
