from django.apps import apps
from django.db.models import Max, Min
from .models import *
from .serializers import  NIFTYAllSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import numpy as np

class ListNiftyGroups(APIView):
    def get(self, request):
        app_models = apps.get_app_config('live_trades').get_models()
        # nifty_models = [model.__name__ for model in app_models if model.__name__.startswith('NIFTY')]
        nifty_models = [model._meta.db_table for model in app_models if model.__name__.startswith('NIFTY')]
        return Response({'nifty_groups': nifty_models})
    
class ScanBollingerBands(APIView):
    def get(self, request, nifty_list='NIFTY_ALL'):
        window = int(request.query_params.get("window", 20))
        num_std_dev = int(request.query_params.get("std_dev", 2))
        percentage_threshold = float(request.query_params.get("percentage", 2.0)) / 100.0
        # Determine list to use
        nifty_list = nifty_list.upper()
        try:
            ModelClass = apps.get_model('live_trades', nifty_list.upper())
            symbols = list(ModelClass.objects.values_list('symbol', flat=True))
        except LookupError:
            return Response(
                {"error": f"Model '{nifty_list}' not found in app 'live_trades'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        industry_filter = request.query_params.get("industry", None)
        upper, lower , result = [], [], []
        for symbol in symbols:
            # Get the latest `window` number of close prices
            historical_prices = StockData.objects.filter(symbol__symbol=symbol).order_by('-date')[:window]
            if len(historical_prices) < window:
                continue  # Skip if not enough data

            if industry_filter and historical_prices[0].symbol.industry.lower() != industry_filter.lower():
                continue  # Skip if industry filter is applied and doesn't match
            prices = [float(data.close) for data in historical_prices]
            latest_close_price = prices[0]  # Most recent close

            # Bollinger Band Calculation
            np_prices = np.array(prices)
            sma = np_prices.mean()
            std_dev = np_prices.std()       
            upper_band = sma + (num_std_dev * std_dev)
            lower_band = sma - (num_std_dev * std_dev)
            try:
                industry = historical_prices[0].symbol.industry
                company = historical_prices[0].symbol.company_name  # Get from related NIFTY_ALL
            except:
                industry = "Unknown"
                company = "Unknown"
            # Check proximity to Bollinger Bands
            if upper_band > 0 and (upper_band * (1 - percentage_threshold) <= latest_close_price <= upper_band * (1 + percentage_threshold)):
                upper.append({
                    "symbol": symbol,
                    "close": round(latest_close_price, 2),
                    "SMA": round(sma, 2),
                    "Upper Band": round(upper_band, 2),
                    "Lower Band": round(lower_band, 2),
                    "proximity": "upper",
                    "industry":industry,
                    "company":company
                })
            elif lower_band > 0 and (lower_band * (1 - percentage_threshold) <= latest_close_price <= lower_band * (1 + percentage_threshold)):
                lower.append({
                    "symbol": symbol,
                    "close": round(latest_close_price, 2),
                    "SMA": round(sma, 2),
                    "Upper Band": round(upper_band, 2),
                    "Lower Band": round(lower_band, 2),
                    "proximity": "lower",
                    "industry":industry,
                    "company":company
                })
        result = {
                "stock_list": nifty_list,"total":len(upper)+len(lower),"upper": upper, "lower": lower}
        return Response(result, status=status.HTTP_200_OK)

class NearATHAPIView(APIView):
    def get(self, request, nifty_list='NIFTY500'):
        try:
            # Get the 'industry' query param, if provided
            industry_filter = request.query_params.get("industry", None)

            # Determine list to use
            nifty_list = nifty_list.upper()
            try:
                # Dynamically fetch the model based on the nifty_list
                ModelClass = apps.get_model('live_trades', nifty_list)
                stocks = ModelClass.objects.all()
            except LookupError:
                return Response(
                    {"error": f"Model '{nifty_list}' not found in app 'live_trades'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Implement logic to find stocks near all-time high
            ath_stocks = []
            for stock in stocks:

                # Apply industry filter if provided
                if industry_filter and stock.industry.lower() != industry_filter.lower():
                    continue  # Skip if the stock's industry doesn't match the filter

                # Fetch all historical stock data for this stock
                stock_data = StockData.objects.filter(symbol=stock.symbol)

                # Determine the all-time high (ATH) for the stock
                ath = stock_data.aggregate(Max('high'))['high__max']

                if ath:  # Ensure ATH is available
                    # Get the most recent stock data for the stock
                    latest_stock = stock_data.latest('date')

                    # Convert ath and close to float for comparison
                    ath_float = float(ath)
                    close_float = float(latest_stock.close)

                    # Compare the current close price to the ATH (e.g., within 90% of ATH)
                    if close_float > 0.9 * ath_float:  # Example threshold
                        # Append stock data along with company and industry information
                        ath_stocks.append({
                            "symbol": latest_stock.symbol.symbol,
                            "close": latest_stock.close,
                            "ath": ath,
                            "company": stock.company_name,  # From NIFTY model
                            "industry": stock.industry,     # From NIFTY model
                            "on_date": latest_stock.date
                        })

            # Return the data directly
            # return Response(ath_stocks, status=status.HTTP_200_OK)
            response_data = {
                "stock_list": nifty_list,
                "total_results": len(ath_stocks),
                "data": ath_stocks
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NearATLAPIView(APIView):
    def get(self, request, nifty_list='NIFTY500'):
        try:
            # Get the 'industry' query param, if provided
            industry_filter = request.query_params.get("industry", None)

            # Determine list to use
            nifty_list = nifty_list.upper()
            try:
                # Dynamically fetch the model based on the nifty_list
                ModelClass = apps.get_model('live_trades', nifty_list)
                stocks = ModelClass.objects.all()
            except LookupError:
                return Response(
                    {"error": f"Model '{nifty_list}' not found in app 'live_trades'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Implement logic to find stocks near all-time low
            atl_stocks = []
            for stock in stocks:
                # Apply industry filter if provided
                if industry_filter and stock.industry.lower() != industry_filter.lower():
                    continue  # Skip if the stock's industry doesn't match the filter

                # Fetch all historical stock data for this stock
                stock_data = StockData.objects.filter(symbol=stock.symbol)

                # Determine the all-time low (ATL) for the stock
                atl = stock_data.aggregate(Min('low'))['low__min']

                if atl:  # Ensure ATL is available
                    # Get the most recent stock data for the stock
                    latest_stock = stock_data.latest('date')

                    # Convert atl and close to float for comparison
                    atl_float = float(atl)
                    close_float = float(latest_stock.close)

                    # Compare the current close price to the ATL (e.g., within 10% of ATL)
                    if close_float < 1.1 * atl_float:  # Example threshold (e.g., 10% above ATL)
                        # Append stock data along with company and industry information
                        atl_stocks.append({
                            "symbol": latest_stock.symbol.symbol,
                            "close": latest_stock.close,
                            "atl": atl,
                            "company": stock.company_name,  # From NIFTY model
                            "industry": stock.industry,     # From NIFTY model
                            "on_date": latest_stock.date
                        })

            response_data = {
                "stock_list": nifty_list,
                "total_results": len(atl_stocks),
                "data": atl_stocks
            }

            return Response(response_data, status=status.HTTP_200_OK)
            # Serialize and return the data
            # return Response(atl_stocks, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TopGainersAPIView(APIView):
    def get(self, request, nifty_list='NIFTY200', days=2):
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "Invalid 'days' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ModelClass = apps.get_model('live_trades', nifty_list.upper())
            stock_list = ModelClass.objects.all()
        except LookupError:
            return Response(
                {"error": f"Model '{nifty_list}' not found in app 'live_trades'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        industry_filter = request.query_params.get("industry", None)
        stock_price_list = []

        for stock in stock_list:
            if industry_filter and stock.industry.lower() != industry_filter.lower():
                continue  # Skip if industry filter is applied and doesn't match

            day_data = StockData.objects.filter(symbol=stock.symbol).order_by('-date')[:days]
            if len(day_data) < days:
                continue

            try:
                latest_day = day_data[0]
                last_day = day_data[::-1][0]
                price_change_in_percentage = (latest_day.close - last_day.close) * 100 / last_day.close
                stock_price_list.append({
                    "symbol": latest_day.symbol.symbol,
                    "gain": price_change_in_percentage,
                    "on_date": latest_day.date,
                    "prev_date": last_day.date,
                    "close": latest_day.close,
                    "prev_close": last_day.close,
                    "company": last_day.symbol.company_name,
                    "industry": last_day.symbol.industry
                })
            except Exception as e:
                print(f"Error processing {stock.symbol}: {e}")
                continue

        # Determine if it's a gainers or losers route
        route_name = request.resolver_match.url_name
        reverse_sort = route_name != "top-losers"  # True for gainers, False for losers

        stock_price_list = sorted(stock_price_list, key=lambda x: x['gain'], reverse=reverse_sort)

        response_data = {
            "total": len(stock_price_list),
            "data": stock_price_list
        }

        return Response(response_data, status=status.HTTP_200_OK)

class StocksByIndustryAPI(APIView):
    def get(self, request, industry_name):
        stocks = NIFTY_ALL.objects.filter(industry=industry_name).order_by('company_name')
        serializer = NIFTYAllSerializer(stocks, many=True)
        # serializer = NIFTYALLSerializer(stocks, many=True)
        return Response(serializer.data)
    
class IndustryListAPI(APIView):
    def get(self, request):
        industries = NIFTY_ALL.objects.values_list('industry', flat=True).distinct().order_by('industry')
        return Response(list(industries))

class StocksAndIndustriesAPI(APIView):
    def get(self, request):
        industry_name = request.GET.get('industry')
        industries = NIFTY_ALL.objects.values_list('industry', flat=True).distinct().order_by('industry')
        stocks = NIFTY_ALL.objects.all()
        if industry_name:
            stocks = stocks.filter(industry=industry_name)
        serializer = NIFTYAllSerializer(stocks, many = True)
        # serializer = NIFTYALLSerializer(stocks, many=True)
        return Response({
            'industries': list(industries),
            'stocks': serializer.data
        })
