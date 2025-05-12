from django.shortcuts import render
from .models import Series

def series_list(request):
    # Получаем списки сериалов по источникам
    tp2_series = Series.objects.filter(source='TP2').order_by('title')
    tp4_series = Series.objects.filter(source='TP4').order_by('title')
    context = {
        'tp2_series': tp2_series,
        'tp4_series': tp4_series,
    }
    return render(request, 'serials/series_list.html', context)
