from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('<int:pk>/', views.job_detail, name='job-detail'),
    path('<int:pk>/apply/', views.apply_to_job, name='job-apply'),
    path('companies/', views.company_list, name='company-list'),
]

# <int:pk> is a URL parameter
# /jobs/1/ → pk=1 will be passed to the view
# /jobs/42/ → pk=42 will be passed to the view