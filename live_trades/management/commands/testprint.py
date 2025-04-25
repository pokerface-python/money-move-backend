import csv
from django.core.management.base import BaseCommand
# from all_data.models import NIFTY100
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import data from a CSV file and create database table for Nifty100 '

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        print('t'*33)
        logger.info(f'Data updated of alltocks from  - up to now successfully')
        print('we are running a print Migration File')
        self.stdout.write(self.style.SUCCESS('Data uploaded to NIFTY100 successfully'))
