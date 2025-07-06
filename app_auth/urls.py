# app_auth/urls.py
from django.urls import path
from app_auth.views import login_view, logout_view, DashboardView 



urlpatterns = [
    # path('', DashboardView.as_view(), name='dashboard'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
]
