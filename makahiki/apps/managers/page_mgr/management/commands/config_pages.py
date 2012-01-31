from django.core import management

def generate_index(page_settings_name):
    """
    page_settings = importlib.import_module(page_settings_name)

    default_layout = page_settings.LAYOUTS["DEFAULT"]
    for row in default_layout:
        for columns in row:
            if isinstance(columns, types.TupleType):
                gamelet = columns[0]
            else:
                gamelet = columns
                break

            view_module_name = 'apps.widgets.'+gamelet+'.views'
            page_views = importlib.import_module(view_module_name)
            view_objects[gamelet] = page_views.supply(request)

    print "-- total %d records loaded" % count

    file.close()
    """

class Command(management.base.BaseCommand):
    help = 'Load the logs files into analytics tables.'

    def handle(self, *args, **options):
      return;