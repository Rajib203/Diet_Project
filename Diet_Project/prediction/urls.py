from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('delete/<int:pk>/', views.delete_prediction, name='delete_prediction'),
    path('inputs/<int:pk>/', views.inputs_view, name='inputs'),
]
