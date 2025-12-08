# realty/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Realtor, Property 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField # <--- Добавьте UsernameField
from django.forms import PasswordInput, TextInput # <--- Добавьте TextInput

# --- 1. ФОРМА РЕГИСТРАЦИИ КЛИЕНТА ---
class ClientSignUpForm(forms.Form):
    # Поля для User
    username = forms.CharField(max_length=150, label='Имя пользователя')
    user_email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль') 
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля') 
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=150, label='Фамилия')
    
    # Поля для Client
    phone = forms.CharField(max_length=20, label='Телефон')
    address = forms.CharField(required=False, widget=forms.Textarea, label='Адрес проживания')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-minimal', 
                'placeholder': field.label 
            })
            
        self.fields['address'].widget.attrs['rows'] = 3

    def clean_password2(self):
        """Проверка, что пароли совпадают."""
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2
    
    def save(self):
        """
        Вручную создает объекты User и Client. 
        Этот метод мы добавили в forms.Form, чтобы чище выглядел views.py.
        """
        # 1. Создаем User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['user_email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.save()
        
        # 2. Создаем Client
        Client.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address'],
        )
        
        return user # Возвращаем объект User для логина

# --- 2. ФОРМА РЕГИСТРАЦИИ РИЕЛТОРА (НЕ АДМИН) ---
class RealtorSignUpForm(UserCreationForm):
    """Форма для регистрации нового риелтора."""
    license_number = forms.CharField(max_length=50, required=True, label='Номер лицензии')
    phone = forms.CharField(max_length=20, required=True, label='Телефон')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=True)
        
        Realtor.objects.create(
            user=user,
            license_number=self.cleaned_data.get('license_number'),
            phone=self.cleaned_data.get('phone'),
            experience_years=0,
        )
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-minimal', 
                'placeholder': field.label 
            })
            

        # self.fields['address'].widget.attrs.update({
        #     'class': 'form-control form-control-minimal',
        #     'rows': 3,
        #     'placeholder': self.fields['address'].label
        # })

# --- 3. ФОРМА УПРАВЛЕНИЯ ОБЪЕКТОМ НЕДВИЖИМОСТИ ---
class PropertyForm(forms.ModelForm):
    
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.HiddenInput(),
        required=False # Ставим False, т.к. мы заполним его в view
    )

    class Meta:
        model = Property
        exclude = ('realtor', 'created_at', 'updated_at', 'is_featured')
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}), # ИСПРАВЛЕНО: area
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}), # ИСПРАВЛЕНО: main_image
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control'}), # ИСПРАВЛЕНО: image1
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}), # ИСПРАВЛЕНО: image2
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}), # ИСПРАВЛЕНО: image3
        }
        
        labels = {
            'title': 'Название объекта',
            'description': 'Описание',
            'price': 'Цена (руб.)',
            'bedrooms': 'Количество спален',
            'bathrooms': 'Количество ванных',
            'area': 'Площадь (м²)', # ИСПРАВЛЕНО: area
            'address': 'Адрес',
            'property_type': 'Тип недвижимости',
            'status': 'Статус',
            'main_image': 'Главное фото', # ИСПРАВЛЕНО: main_image
            'image1': 'Изображение 1', # ИСПРАВЛЕНО: image1
            'image2': 'Изображение 2', # ИСПРАВЛЕНО: image2
            'image3': 'Изображение 3', # ИСПРАВЛЕНО: image3
        }

class LoginForm(AuthenticationForm):
    # Явно переопределяем поля и виджеты, чтобы применить наш класс стилей
    username = UsernameField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-minimal', 
            'placeholder': 'Имя пользователя',
        }),
        label='Имя пользователя'
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control form-control-minimal', 
            'placeholder': 'Пароль',
        })
    )
    
    # Теперь __init__ может быть пустым или использоваться для других целей, 
    # но явное определение выше — это лучший способ гарантировать применение классов.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Явно устанавливаем виджеты, чтобы гарантировать, что мы используем наши атрибуты.
        # Это должно устранить проблему с переопределением стилей.
        self.fields['username'].widget = TextInput(attrs={
            'class': 'form-control form-control-minimal', 
            'placeholder': self.fields['username'].label,
        })
        
        self.fields['password'].widget = PasswordInput(attrs={
            'class': 'form-control form-control-minimal', 
            'placeholder': self.fields['password'].label,
        })
        
        # 2. Дополнительная гарантия: переименование меток на русский
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'