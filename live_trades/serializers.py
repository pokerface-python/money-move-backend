# serializers.py
from rest_framework import serializers
from .models import NIFTY_ALL, StockData

class NIFTYBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIFTY_ALL
        fields = ['symbol', 'company_name', 'industry']

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
        read_only_fields = ['symbol']  # Make 'symbol' read-only

class NIFTYAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIFTY_ALL
        fields = ['symbol', 'company_name', 'industry']
     