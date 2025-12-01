from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
]