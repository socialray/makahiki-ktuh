"""handles request for flot widget."""
from apps.widgets.status.users.views import remote_supply
from apps.widgets.status.models import DailyStatus


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    new_user_data = []
    daily_login_data = []
    result = remote_supply(request, page_name)
    result = result['logins']
    template_date_format = "%m/%d"

    for item in result:
        point = {'x': item['date'], 'y': item['logins']}
        new_user_data.append(point)

    new_user_series = {
      'color': "#000",
      'show': 'true',
      'data': new_user_data,
    }

    for item in DailyStatus.objects.all():
        point = {'x': item.date.strftime(template_date_format), 'y': item.daily_visitors}
        daily_login_data.append(point)

    daily_login_series = {
      'color': "#000",
      'show': 'true',
      'data': daily_login_data,
    }
    data_sets = {
                'New Users': new_user_series,
               'Daily Logins': daily_login_series
    }

    xaxis_color = "#000"

    return {
        "data_sets": data_sets,
        "xaxis_color": xaxis_color,
    }
