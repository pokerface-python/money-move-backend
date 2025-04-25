import csv
from django.core.management.base import BaseCommand
from live_trades.models import NIFTY_ALL
from django.apps import apps 

class Command(BaseCommand):
    help = 'Import data from a CSV file and create database table for Nifty500 '

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', required=True, type=str, help='Path to the CSV file')
        parser.add_argument('--table', required= True, type=str, help='Name of the table to import data into')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        model_name = options['table']

        try:
            ModelClass = apps.get_model('live_trades', model_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(f'Model "{model_name}" does not exist in app "live_trades".'))
            return
        
        if not ModelClass:
            self.stdout.write(self.style.ERROR(f'Table {model_name} is not supported'))
            return
        

        with open(csv_file_path, 'r') as csv_file:
            read_data = csv.DictReader(csv_file)
            for row in read_data:
                ModelClass.objects.create(
                    symbol=row.get('Symbol'),
                    company_name=row.get('Company Name'),
                    industry=row.get('Industry')
                )

        self.stdout.write(self.style.SUCCESS(f'Data uploaded to {model_name} successfully'))

# /*******  b3f465ee-69d2-4909-90d6-db9cd10d0224  *******/

#     def handle(self, *args, **options):
#         csv_file_path = options['csv_file']

#         with open(csv_file_path,'r') as csv_file:
#             read_data = csv.DictReader(csv_file)
#             for row in read_data:
#                 NIFTY_ALL.objects.create(
#                     symbol = row.get('Symbol'),
#                     company_name = row.get('Company Name'),
#                     industry = row.get('Industry')
#                 )

#         self.stdout.write(self.style.SUCCESS('Data uploaded to NIFTY_ALL successfully'))
