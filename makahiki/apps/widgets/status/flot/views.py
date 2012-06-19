"""handles request for flot widget."""
from apps.widgets.status.users.views import remote_supply


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    data = []
    result = remote_supply(request, page_name)
    result = result['logins']
    for item in result:
        point = {'x': item['date'], 'y': item['logins']}
        data.append(point)

    series = {
      'color': "#000",
      'fill_color': "#fff",
      'show': 'true',
      'data': data,
    }

    #As long as titles are different, it's possible to define
    # multiple data sets and add them to data_sets.

    data_sets = {
      'Title goes here': series
    }

    #Axis Definitions

    #Example of text labels instead of numerics
    # xaxis_ticks= {
    #   min: 0,
    #   ticks: [
    #      [0, ""],
    #      [1, "hello"],
    #      [2, "hi"],
    #      [3, "helloagain"]
    #   ],
    #   max: 3
    # }

    #Exampel of date labels:
   # xaxis_ticks= [
   #     [new Date("2007/05/19"), 3],
   #     [new Date("2007/05/20"), 17],
   #     [new Date("2007/05/21"), 10]
   # ]

    yaxis_color = "#000"
    yaxis_ticks = [1, 5, 10, 15, 20, 25]

    xaxis_color = "#000"
    xaxis_ticks = ""
    time_format = "%m/%d"

    return {
        "data_sets": data_sets,
        "border_width": '0',
        "show_legend": 'false',
        "yaxis_ticks": yaxis_ticks,
        "yaxis_color": yaxis_color,
        "xaxis_ticks": xaxis_ticks,
        "xaxis_color": xaxis_color,
        "xaxis_mode": "time",
        "yaxis_mode": "",
        "time_format": time_format
    }
