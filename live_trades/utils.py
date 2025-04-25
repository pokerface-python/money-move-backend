from django.conf import settings
from datetime import datetime
import yfinance as yf
from .models import StockData,NIFTY500, NIFTY_ALL
from django.db.utils import IntegrityError

def store_all_stock_data(stock_symbol,start_date,end_date):
    print('saving data for stock ',stock_symbol)
    if not start_date:
        start_date = settings.START_DATE  # Use default start date if not provided

    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d') 

    
    # end_date = datetime.now().strftime('%Y-%m-%d')
    retrieved_data = yf.download(f'{stock_symbol}.NS', start=start_date, end=end_date)
    
    stock = NIFTY_ALL.objects.get(symbol = stock_symbol)

    for index,row in retrieved_data.iterrows():
    
        # warning fix pandas
        open = float(round(row['Open'].iloc[0], 2))
        high = float(round(row['High'].iloc[0], 2))
        low = float(round(row['Low'].iloc[0], 2))
        close = float(round(row['Close'].iloc[0], 2))
        volume = int(row['Volume'].iloc[0])




        # date = datetime.strptime(str(index), "%Y-%m-%d %H:%M:%S")
        date = index.date()
        try:
            stock_object,created = StockData.objects.get_or_create(symbol = stock,open = open,high = high,low = low,close = close,date = date,volume = volume)
            if not created:
            # If the entry already existed, update it
                stock_object.open = open
                stock_object.high = high
                stock_object.low = low
                stock_object.close = close
                stock_object.volume = volume
                stock_object.save()
                # print('saved succesffuluy ',stock,' <-stock and date -> ',date)

        # Optional: Add a breakpoint or logging to see what's happening
        except IntegrityError:
            
            # print('intigrity error for ',stock)
            continue
    print(f"Processed {stock_symbol} for date {end_date}: {stock_object}")


