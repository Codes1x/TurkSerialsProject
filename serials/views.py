from django.shortcuts import render
from .models import Series

def series_list(request):
    tp2_series = Series.objects.filter(source='TP2').order_by('title')
    tp3_series = Series.objects.filter(source='TP3').order_by('title')

    return render(request, 'serials/series_list.html', {
        'tp2_series': tp2_series,
        'tp3_series': tp3_series
    })
