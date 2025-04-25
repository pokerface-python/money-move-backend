from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('scan-bb/',ScanBollingerBands.as_view(), name='ScanBollingerBands'),
    path('scan-bb/<str:nifty_list>/',ScanBollingerBands.as_view(), name='ScanBollingerBands'),
    # http://127.0.0.1:8000/api/scan-bb/?industry=Financial%20Services

    path('nifty-groups/', ListNiftyGroups.as_view()),

    # near all time high and low
    path('near-ath/', NearATHAPIView.as_view(), name='near-ath'),
    path('near-ath/<str:nifty_list>/', NearATHAPIView.as_view(), name='near-ath'),
    path('near-atl/', NearATLAPIView.as_view(), name='near-atl'),
    path('near-atl/<str:nifty_list>/', NearATLAPIView.as_view(), name='near-atl'),
    
    # top gainers with nifty list and days as filters
    path('top-gainers/', TopGainersAPIView.as_view(), name='top-gainers-default'),
    path('top-gainers/<str:nifty_list>/', TopGainersAPIView.as_view(), name='top-gainers-list'),
    path('top-gainers/<str:nifty_list>/<int:days>/', TopGainersAPIView.as_view(), name='top-gainers-days'),
    # top losers list 
    path('top-losers/', TopGainersAPIView.as_view(), name='top-losers'),
    path('top-losers/<str:nifty_list>/', TopGainersAPIView.as_view(), name='top-losers'),
    path('top-losers/<str:nifty_list>/<int:days>/', TopGainersAPIView.as_view(), name='top-losers'),
    # sort by industry name will work with kind of below urls
    # http://localhost:8000/api/top-gainers/nifty100/20/?industry=Power

    # sort by industry 
    path('industries/', IndustryListAPI.as_view(), name='api_industry_list'),
    path('stocks/industry/<str:industry_name>/', StocksByIndustryAPI.as_view(), name='api_stocks_by_industry'),
    path('stocks-industries/', StocksAndIndustriesAPI.as_view(), name='api_stocks_and_industries'),
]


