from django.contrib import admin
from .models import Client, Realtor, Property

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['created_at']

@admin.register(Realtor)
class RealtorAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'phone', 'experience_years']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'license_number']
    list_filter = ['experience_years', 'created_at']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'status', 'price', 'realtor', 'created_at']
    list_filter = ['property_type', 'status', 'is_featured', 'created_at']
    search_fields = ['title', 'address', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'property_type', 'status')
        }),
        ('Детали объекта', {
            'fields': ('address', 'price', 'area', 'bedrooms', 'bathrooms')
        }),
        ('Участники', {
            'fields': ('realtor', 'client')
        }),
        ('Изображения', {
            'fields': ('main_image', 'image1', 'image2', 'image3', 'is_featured')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )