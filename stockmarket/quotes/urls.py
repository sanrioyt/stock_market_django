from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('list_stocks/', views.list_stocks, name='list_stocks'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('import_stock_data/', views.import_stock_data, name='import_stock_data'),
    path('graph_stocks/', views.graph_stocks, name='graph_stocks'),
]
