import numpy as np
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib import messages

from plotly.graph_objs import Figure
import plotly.offline as pyo

from .models import Stock, HistoricalQuote
from .forms import StockForm


def home(request):
    """ Returns home """
    return render(request, 'quotes/home.html')


def about(request):
    """Displays about statement of website"""
    return render(request, 'quotes/about.html')


def list_stocks(request):
    """Dislays all stocks in alphabetical order"""
    stocks = Stock.objects.all().order_by('ticker')
    return render(request, 'quotes/list_stocks.html', {'stocks': stocks})


def add_stock(request):
    """adds a stock to the database"""
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been successfully added"))
            return redirect('list_stocks')
    else:
        form = StockForm()
        return render(request, 'quotes/add_stock.html', {'form': form})

def import_stock_data(request):
    tickers = ['AAPL', 'INTC', 'VZ', 'WMT']
    for ticker in tickers:
        df = pd.read_csv(f'data/{ticker}.csv', parse_dates=['Date'])
        stock = Stock.objects.get(ticker=ticker)
        for i in range(len(df)):
            historical_q = HistoricalQuote(ticker=stock, date=df.loc[i, "Date"], price=df.loc[i, "AdjClose"])
            historical_q.save()
    messages.success(request, ("Successfully added historical quotes for AAPL, INTC, VZ, and WMT"))
    return redirect('home')


def graph_stocks(request):
    """Displays a graph of 3 stocks using plotly"""
    aapdf = pd.read_csv('data/AAPL.csv', parse_dates=['Date'])
    intcdf = pd.read_csv('data/INTC.csv', parse_dates=['Date'])
    wmtdf = pd.read_csv('data/WMT.csv', parse_dates=['Date'])

    aapl_trace = {'type': 'scatter',
                 'x': aapdf['Date'],
                 'y': aapdf['AdjClose'],
                 'mode': 'lines+markers',
                 'name': 'AAPL',
                 'marker': {'color': 'red'},
                 }

    intc_trace = {'type': 'scatter',
                   'x': aapdf['Date'],
                   'y': intcdf['AdjClose'],
                   'mode': 'lines+markers',
                   'name': 'INTC',
                   'marker': {'color': 'blue'},
                }

    wmt_trace = {'type': 'scatter',
                 'x': aapdf['Date'],
                 'y': wmtdf['AdjClose'],
                 'mode': 'lines+markers',
                 'name': 'WMT',
                 'marker': {'color': 'green'},
        }

    layout = {
        'title': '<b>Adjusted Close for APPL, INTC and WMT from 2020/06/08 till 2021/06/04',
        'hovermode': 'closest',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Price in $'}
    }

    data = [aapl_trace, intc_trace, wmt_trace]
    figure = Figure(data=data, layout=layout)

    div = pyo.plot(figure, filename='line1.html', auto_open=False, output_type='div')

    return render(request, 'quotes/graph_stocks.html', {'graph': div})
