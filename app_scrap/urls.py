# app_auth/urls.py
from django.urls import path
from app_scrap import views 



urlpatterns = [
    path('dashboard/', views.change_dashboard, name='change_dashboard'),
    
    path('change_history/', views.change_history, name='change_history'),
    path('pull_detail/<int:pull_id>/', views.pull_detail, name='pull_detail'),
    path('start-processing/', views.start_data_processing, name='start_processing'), 
    
    path('latest-cia-data/', views.latest_data_pull_view, name='cia_data_list'),

]
