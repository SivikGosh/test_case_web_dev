from datetime import datetime


def current_month(request):
    return {'current_month': datetime.now().month}
