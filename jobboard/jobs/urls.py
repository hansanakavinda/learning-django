from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'applications', views.ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register),
    path('auth/login/', views.login),
    path('auth/logout/', views.logout),
]