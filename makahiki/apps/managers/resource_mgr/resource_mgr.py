"""resource manager module"""
import datetime


def team_current_energy_data(team):
    """Return the latest energy data of the current date."""
    date = datetime.date.today()
    data = team.energydata_set.filter(date=date)
    if data:
        return data[0]
    else:
        return None


def team_current_energy_usage(team):
    """Return the latest energy data of the current date."""
    data = team_current_energy_data(team)
    if data:
        return data.usage
    else:
        return 0
