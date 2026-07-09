from django.urls import path
from . import views       



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
    path('dashboard/', views.history_view, name='dashboard'),
    path('delete/<int:pk>/', views.delete_prediction, name='delete_prediction'),
    path('inputs/<int:pk>/', views.inputs_view, name='inputs'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('api/weekly-chart/', views.api_weekly_chart, name='api_weekly_chart'),
    path('api/history/', views.api_history, name='api_history'),
    path('api/delete-history/<int:pk>/', views.api_delete_history, name='api_delete_history'),
]
