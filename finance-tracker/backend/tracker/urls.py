

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.UploadCSVView.as_view(), name='upload_csv'),
    path('set-budget/', views.BudgetView.as_view(), name='set_budget'),
    # path('login/', views.login, name='login'),
    # path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout, name='logout'),
    path('filter-transactions/', views.filter_transactions, name='filter_transactions'),
]