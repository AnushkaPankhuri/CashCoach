from django.contrib import admin
from django.urls import path
from .views import UploadCSV
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('upload/', UploadCSV.as_view(), name='upload_csv'),
    # path('upload/', views.UploadCSV, name='upload_csv'),
    path('transactions/', views.all_transactions, name='all_transactions'),
    path('transactions/filter/', views.filter_transactions, name='filter_transactions'),
    path('transactions/summary/', views.summary, name='summary'),
    path('api/get-insights/', views.get_insights, name='get_insights'),
    path('set_budget/', views.set_budget_threshold, name='set_budget')
]