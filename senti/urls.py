from django.urls import path

from . import views

urlpatterns = [
    path('search', views.search, name='search-url'),
    path('chart', views.chart, name='chart-url'),
    path('subtitle', views.subtitles, name='subtitles-url')
]
