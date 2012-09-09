"""handles request for user gchart widget."""
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.status.models import DailyStatus


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    #todays_users = Profile.objects.filter(last_visit_date=datetime.datetime.today())

    rounds_info = challenge_mgr.get_all_round_info()
    start = rounds_info["competition_start"]
    daily_status = DailyStatus.objects.filter(short_date__gte=start).order_by('short_date')
    prior_day_users = 0
    for status in daily_status:
        status.display_date = "%d/%d" % (status.short_date.month, status.short_date.day)
        status.new_users = status.setup_users - prior_day_users
        prior_day_users = status.setup_users

    return {
        "daily_status": daily_status,
    }
