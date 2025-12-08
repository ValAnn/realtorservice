from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm 

urlpatterns = [
    path('', views.home, name='home'),
    # path('accounts/login/', auth_views.LoginView.as_view(
    #     template_name='realty/login.html', 
    #     authentication_form=LoginForm
    # ), name='login'),
    
    # # 2. Выход из системы (Стандартный Django Logout)
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
    
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),

    path('signup/client/', views.client_signup, name='client_signup'),
    path('signup/realtor/', views.realtor_signup, name='realtor_signup'),

    path('dashboard/', views.realtor_dashboard, name='realtor_dashboard'),

    path('property/add/', views.property_add, name='property_add'), 

    path('property/edit/<int:pk>/', views.property_edit, name='property_edit'),
    path('property/delete/<int:pk>/', views.property_delete, name='property_delete'),

    # path('accounts/login/', auth_views.LoginView.as_view(
    #     template_name='realty/login.html', 
    #     authentication_form=LoginForm # <-- Используем нашу кастомную форму
    # ), name='login'),
    
    
]