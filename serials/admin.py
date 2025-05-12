from django.contrib import admin
from .models import Series

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'url')
    search_fields = ('title', 'source')
    list_filter = ('source',)
