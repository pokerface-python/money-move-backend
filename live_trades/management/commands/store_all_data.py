import csv
from django.core.management.base import BaseCommand
from live_trades.models import NIFTY500, NIFTY_ALL
from django.conf import settings
from live_trades.utils import store_all_stock_data
import logging
# logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Get Latest data of All stocks of NIFTY 500 '

    def add_arguments(self, parser):
        """Accept start and end date as optional arguments."""
        parser.add_argument('--start', type=str, help='Start date in YYYY-MM-DD format')
        parser.add_argument('--end', type=str, help='End date in YYYY-MM-DD format')


    def handle(self, *args, **options):
        start_date = options.get('start')
        end_date = options.get('end')

        try:
            print("Trying to save all stock data into the database")
            all_500_stocks = NIFTY_ALL.objects.all()
            # count = 0̃
            print(f"Fetching stock data from {start_date} to {end_date}")
            for stock in all_500_stocks:

                try:
                    
                    store_all_stock_data(stock.symbol,start_date,end_date)
                except Exception as e:
                    print('exception in store all data mgmt command : ',e)
                    pass
            self.stdout.write(self.style.SUCCESS(f'Data updated of all {len(all_500_stocks)-1} stocks from {settings.START_DATE} - upto now successfully'))
        except Exception as e:
            print('exception in store all data mgmt command : ',e)
            pass

        