from django.shortcuts import render, get_object_or_404
from .models import Series, Article

def series_list(request):
    series = Series.objects.all()
    return render(request, 'serials/series_list.html', {'series': series})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'serials/article.html', {'article': article})
