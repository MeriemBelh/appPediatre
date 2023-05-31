from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('test/', include('testExample.urls')),
    path('', views.testIndex, name='testIndex'),
    path('selectAJAX/', views.selectAJAX, name='selectAJAX'),
    path('selectAJAX_view/', views.selectAJAX_view, name='selectAJAX_view'),
    path('Pie_chart_1/', views.Pie_chart_1, name='Pie_chart_1'),
    path('Pie_chart_2/', views.Pie_chart_2, name='Pie_chart_2'),
    path('Pie_chart_3/', views.Pie_chart_3, name='Pie_chart_3'),
    path('pie_chart_view/', views.pie_chart_view, name='pie_chart_view'),
    path('line_chart/', views.line_chart, name='line_chart'),
    path('line_chart_poids/', views.line_chart_poids, name='line_chart_poids'),
    path('line_chart_all/', views.line_chart_all, name='line_chart_all'),
    path('line_chart_all_view/', views.line_chart_all_view, name='line_chart_all_view'),
]