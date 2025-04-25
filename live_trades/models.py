from django.db import models
class NIFTYBase(models.Model):
    symbol = models.CharField(max_length=10, unique = True)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    def save(self,*args,**kwargs):
            self.symbol = self.symbol.upper()
            super().save(*args,**kwargs)

    def __str__(self):
        return self.symbol

    class Meta:
        abstract = True

class NIFTY50(NIFTYBase):
    class Meta:
        db_table = 'NIFTY50'
        
class NIFTY100(NIFTYBase):
    class Meta:
        db_table = 'NIFTY100'

class NIFTY200(NIFTYBase):
    class Meta:
        db_table = 'NIFTY200'

class NIFTY500(NIFTYBase):
    class Meta:
        db_table = 'NIFTY500'    

class NIFTYMIDCAP50(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_MIDCAP50'
class NIFTYMIDCAP100(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_MIDCAP100'

class NIFTYMIDCAP150(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_MIDCAP150'
class NIFTYSMALLCAP50(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_SMALLCAP50'
class NIFTYSMALLCAP100(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_SMALLCAP100'
class NIFTYSMALLCAP250(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_SMALLCAP250'

class NIFTYMICROCAP250(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_MICROCAP250'

class NIFTYNEXT50(NIFTYBase):
    class Meta:
        db_table = 'NIFTY_NEXT50'

class NIFTY_ALL(NIFTYBase):
    class Meta:
        db_table = "NIFTY_ALL"

class StockData(models.Model):
    symbol = models.ForeignKey(NIFTY_ALL, to_field = 'symbol',db_column="stock_symbol", on_delete= models.PROTECT)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.PositiveIntegerField()

    class Meta:
        unique_together = ['symbol','date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.symbol} - {self.date}"

class IndexData(models.Model):
    symbol = models.CharField(max_length=15)
    date = models.DateTimeField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.PositiveIntegerField()

