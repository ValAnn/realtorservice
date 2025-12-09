from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    """Модель клиента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"

class Realtor(models.Model):
    """Модель риелтора"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    license_number = models.CharField(max_length=50, verbose_name="Номер лицензии", unique=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    experience_years = models.IntegerField(default=0, verbose_name="Опыт работы (лет)")
    bio = models.TextField(verbose_name="О себе", blank=True)
    photo = models.ImageField(upload_to='realtors/', verbose_name="Фотография", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Риелтор"
        verbose_name_plural = "Риелторы"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Лицензия: {self.license_number}"

class Property(models.Model):
    """Модель объекта недвижимости"""
    
    # Типы недвижимости
    PROPERTY_TYPES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('commercial', 'Коммерческая недвижимость'),
        ('land', 'Земельный участок'),
    ]
    
    # Статусы
    STATUS_CHOICES = [
        ('for_sale', 'Продажа'),
        ('for_rent', 'Аренда'),
        ('sold', 'Продано'),
        ('rented', 'Сдано в аренду'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, verbose_name="Тип недвижимости")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='for_sale', verbose_name="Статус")
    address = models.TextField(verbose_name="Адрес")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    area = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Площадь (м²)")
    bedrooms = models.IntegerField(verbose_name="Количество спален", default=0)
    bathrooms = models.IntegerField(verbose_name="Количество ванных комнат", default=0)
    
    # Внешние ключи
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, related_name='properties', verbose_name="Риелтор")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='properties', verbose_name="Клиент")
    
    # Изображения
    main_image = models.ImageField(upload_to='properties/main/', verbose_name="Главное изображение", blank=True, null=True)
    image1 = models.ImageField(upload_to='properties/', verbose_name="Изображение 1", blank=True, null=True)
    image2 = models.ImageField(upload_to='properties/', verbose_name="Изображение 2", blank=True, null=True)
    image3 = models.ImageField(upload_to='properties/', verbose_name="Изображение 3", blank=True, null=True)
    
    # Дополнительные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    
    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_property_type_display()} - {self.price}"