from django.contrib import admin
from django.urls import path
from .views import UploadCSV
from . import views

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.UploadCSVView.as_view(), name='upload_csv'),
    path('set-budget/', views.BudgetView.as_view(), name='set_budget'),
]