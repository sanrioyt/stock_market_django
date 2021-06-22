from django.db import models

class Stock(models.Model):
    """Model that describes a particular stock"""
    ticker = models.CharField(max_length=20)
    description = models.CharField(max_length=100, default='', blank=True)
    sector = models.CharField(max_length=80)
    marketCap = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.ticker


class HistoricalQuote(models.Model):
    """Model that has quote for a particular stock"""
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    class Meta:
        unique_together = [['ticker', 'date']]

    def __str__(self):
        return f"{self.ticker} - {self.date} - ${self.price:.2f}"

    class Meta:
        ordering=['date', 'ticker']
