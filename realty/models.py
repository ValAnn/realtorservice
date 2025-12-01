from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Email")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Realtor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя риелтора")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Номер лицензии")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Риелтор"
        verbose_name_plural = "Риелторы"

class Property(models.Model):
    # Поля для объекта недвижимости
    address = models.CharField(max_length=255, unique=True, verbose_name="Адрес")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    area = models.FloatField(verbose_name="Площадь (кв.м)")
    description = models.TextField(blank=True, verbose_name="Описание")

    # Связи: Объект привязан к одному риелтору
    realtor = models.ForeignKey(
        Realtor, 
        on_delete=models.SET_NULL, # Что делать при удалении риелтора (установить NULL)
        null=True, 
        blank=True, 
        related_name='properties',
        verbose_name="Риелтор"
    )

    # Связь: Какой клиент заинтересован в объекте (можно сделать и через отдельную модель 'Сделка')
    # Сейчас сделаем как "ответственный клиент", для простоты
    responsible_client = models.ForeignKey(
        Client, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='desired_properties',
        verbose_name="Ответственный клиент"
    )

    is_available = models.BooleanField(default=True, verbose_name="Доступен для продажи/аренды")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"