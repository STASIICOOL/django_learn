from django.core.management.base import BaseCommand, CommandError
from locations.models import Country
import re

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('search', type=str, help=u'world for file countries')

    def handle(self, *args, **options):
        search = options['search']
        countries = Country.objects.all()
        for country in countries:
            country_name = country.name
            search_status = re.search(search, country_name)
            if search_status:
                print(country_name)

