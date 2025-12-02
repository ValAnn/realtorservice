# realty/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Realtor, Property # Импортируем все необходимые модели!

# --- 1. ФОРМА РЕГИСТРАЦИИ КЛИЕНТА ---
class ClientSignUpForm(UserCreationForm):
    """Форма для регистрации нового клиента."""
    phone = forms.CharField(max_length=20, required=True, label='Телефон')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Адрес проживания')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        
        # Добавляем стили Bootstrap для базовых полей
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Сохраняем пользователя (User)
        user = super().save(commit=commit)
        # Создаем связанный объект Client
        Client.objects.create(
            user=user,
            phone=self.cleaned_data.get('phone'),
            address=self.cleaned_data.get('address'),
        )
        return user

# --- 2. ФОРМА РЕГИСТРАЦИИ РИЕЛТОРА (НЕ АДМИН) ---
class RealtorSignUpForm(UserCreationForm):
    """Форма для регистрации нового риелтора."""
    license_number = forms.CharField(max_length=50, required=True, label='Номер лицензии')
    phone = forms.CharField(max_length=20, required=True, label='Телефон')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

        # Добавляем стили Bootstrap для базовых полей
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=True) # Сохраняем как обычного пользователя (is_staff=False)
        
        # Создаем связанный объект Realtor
        Realtor.objects.create(
            user=user,
            license_number=self.cleaned_data.get('license_number'),
            phone=self.cleaned_data.get('phone'),
            experience_years=0,
        )
        return user

# --- 3. ФОРМА УПРАВЛЕНИЯ ОБЪЕКТОМ НЕДВИЖИМОСТИ ---
class PropertyForm(forms.ModelForm):
    """Форма для добавления и редактирования объектов недвижимости риелтором."""
    class Meta:
        model = Property
        # Исключаем поля, которые заполняются автоматически (realtor, created_at, updated_at) 
        # или заполняются только администратором (is_featured)
        exclude = ('realtor', 'created_at', 'is_featured', 'updated_at')
        
        # Применяем классы Bootstrap и настройки виджетов
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'square_feet': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            # photo_main не требует класса form-control, так как это FileInput
        }
        
        labels = {
            'title': 'Название объекта',
            'description': 'Описание',
            'price': 'Цена (руб.)',
            'bedrooms': 'Количество спален',
            'bathrooms': 'Количество ванных',
            'square_feet': 'Площадь (кв. м.)',
            'address': 'Адрес',
            'city': 'Город',
            'state': 'Регион',
            'zipcode': 'Индекс',
            'property_type': 'Тип недвижимости',
            'status': 'Статус',
            'photo_main': 'Главное фото',
        }