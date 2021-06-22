from django.contrib import admin

from .models import Stock, HistoricalQuote

class HistoricalQuoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['date', 'ticker', 'price']
    list_filter = ['ticker',]

admin.site.register(Stock)
admin.site.register(HistoricalQuote, HistoricalQuoteAdmin)
