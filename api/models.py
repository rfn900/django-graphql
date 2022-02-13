from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    initial_account_balance = models.IntegerField()
    account_balance = models.IntegerField()

    def __str__(self):
        return self.name


class Trade(models.Model):
    BUY = 'B'
    SELL = 'S'

    TRADE_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell')
    ]

    price = models.IntegerField()
    volume = models.IntegerField()
    trade_type = models.CharField(max_length=1, choices=TRADE_TYPE_CHOICES)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,
                                  related_name='trades')
    date_created = models.DateField(auto_now_add=True)
    stock_symbol = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['-date_created']
