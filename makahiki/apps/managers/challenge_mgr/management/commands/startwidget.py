"""
Creates a Makahiki widget directory structure for the given name. The widget will be
created under the apps/widgets directory.

"""

from django.core import management
from apps.utils import widget_utils

doc_string = __doc__


class Command(management.base.BaseCommand):
    """command"""
    help = doc_string
    args = "<widget_name>"

    def handle(self, *args, **options):
        """set up the test data"""

        if len(args) == 0:
            self.stdout.write("The widget name is required.\n")
            return

        name = args[0]

        widget_utils.create_widget(name)
