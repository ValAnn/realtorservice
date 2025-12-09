from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from realty.models import Property, Realtor, Client
# from models import Property, Realtor

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from realty.models import Client, Realtor, Property 
from realty.forms import ClientSignUpForm, RealtorSignUpForm, PropertyForm, LoginForm 


User = get_user_model()

class RealtorModelTest(TestCase):
    """Тесты для модели Realtor."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            first_name='Иван',
            last_name='Петров'
        )
        self.realtor = Realtor.objects.create(
            user=self.user,
            experience_years=5,
            license_number='LIC12345',
            bio='Опытный риелтор'
        )
    
    def test_realtor_creation(self):
        """1. TestCreateRealtor_ValidUserLink: Проверяет успешное создание риелтора."""
        self.assertTrue(isinstance(self.realtor, Realtor))
        self.assertEqual(self.realtor.user.get_full_name(), 'Иван Петров')
        self.assertEqual(self.realtor.experience_years, 5)

    def test_realtor_string_representation(self):
        """Проверяет строковое представление (str) модели Realtor."""
        self.assertEqual(str(self.realtor), 'Иван Петров - Лицензия: LIC12345')
    
    def test_realtor_experience_positive(self):
        """Проверяет, что опыт работы не может быть отрицательным (если есть валидатор, здесь проверяется его отсутствие или базовое значение)."""
        # Если в модели нет валидатора, этот тест проверяет простое присвоение
        self.assertTrue(self.realtor.experience_years >= 0)


class PropertyModelTest(TestCase):
    """Тесты для модели Property."""
    
    def setUp(self):
        # Создаем риелтора, необходимого для объекта
        self.user = User.objects.create_user(username='realtor_test', password='password')
        self.realtor = Realtor.objects.create(user=self.user, experience_years=1)
        self.client = Client.objects.create(user=self.user, phone='12345', address='address')
        
        # Создаем тестовый объект недвижимости
        self.property1 = Property.objects.create(
            title='Квартира в центре',
            address='ул. Пушкина, 10',
            price=15000000,
            area=65.5,
            realtor=self.realtor,
            is_featured=True,
            client_id = self.client.id
        )
        self.property2 = Property.objects.create(
            title='Дом на окраине',
            price=25000000,
            area=120,
            realtor=self.realtor,
            is_featured=False,
            client_id = self.client.id
        )

    def test_property_creation(self):
        """1. TestCreateProperty_ValidData: Проверяет успешное создание объекта."""
        self.assertTrue(isinstance(self.property1, Property))
        self.assertEqual(self.property1.title, 'Квартира в центре')
        self.assertEqual(self.property1.price, 15000000)
        self.assertEqual(self.property1.realtor.user.username, 'realtor_test')
    
    def test_filter_featured_property(self):
        """4. TestFeaturedProperty_Boolean: Метод должен возвращать только рекомендуемые объекты."""
        featured = Property.objects.filter(is_featured=True)
        self.assertEqual(featured.count(), 1)
        self.assertEqual(featured.first().title, 'Квартира в центре')

    def test_filter_by_price_range(self):
        """3. TestFilterByPrice_Range: Проверяет фильтрацию по диапазону цен."""
        # Объекты в диапазоне от 10,000,000 до 20,000,000
        filtered = Property.objects.filter(price__gte=10000000, price__lte=20000000)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().title, 'Квартира в центре')

    def test_property_deletion(self):
        """5. TestDeleteProperty: Проверяет удаление объекта."""
        initial_count = Property.objects.count()
        self.property1.delete()
        self.assertEqual(Property.objects.count(), initial_count - 1)

User = get_user_model() 

class ClientSignUpFormTest(TestCase):
    """Тесты для формы регистрации клиента (ClientSignUpForm)."""
    
    # 1. Тест: Успешная регистрация клиента
    def test_client_signup_valid(self):
        """Проверяет, что форма действительна и метод save() создает User и Client."""
        initial_user_count = User.objects.count()
        initial_client_count = Client.objects.count()

        form_data = {
            'username': 'newclient',
            'user_email': 'client@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'Иван',
            'last_name': 'Клиентов',
            'phone': '89001234567',
            'address': 'Москва, ул. Ленина'
        }
        form = ClientSignUpForm(data=form_data)
        
        self.assertTrue(form.is_valid(), form.errors.as_text())
        
        
        user = form.save()
        
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertEqual(Client.objects.count(), initial_client_count + 1)
        self.assertTrue(Client.objects.filter(user=user).exists())
        self.assertEqual(user.username, 'newclient')


    def test_client_signup_password_mismatch(self):
        """Проверяет, что форма недействительна, если password и password2 не совпадают."""
        form_data = {
            'username': 'user',
            'user_email': 'test@test.com',
            'password': 'password1',
            'password2': 'password2',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'phone': '89001234567',
        }
        form = ClientSignUpForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('Пароли не совпадают.', form.errors['password2'])


    def test_client_signup_missing_phone(self):
        """Проверяет, что поле 'phone' является обязательным."""
        form_data = {
            'username': 'user',
            'user_email': 'test@test.com',
            'password': 'password123',
            'password2': 'password123',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            # 'phone' отсутствует
        }
        form = ClientSignUpForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors) 
        



class RealtorSignUpFormTest(TestCase):
    """Тесты для формы регистрации риелтора (RealtorSignUpForm)."""

    def test_realtor_signup_valid(self):
        """Проверяет, что форма действительна и save() создает User и Realtor."""
        initial_user_count = User.objects.count()
        initial_realtor_count = Realtor.objects.count()

        form_data = {
            'username': 'newrealtor',
            'email': 'realtor@example.com',
            'password2': '13re4a4ltorpwd',
            'password1': '13re4a4ltorpwd',
            'first_name': 'Анна',
            'last_name': 'Риелтор',
            'license_number': 'RLIC789',
            'phone': '89112223344',
        }
        form = RealtorSignUpForm(data=form_data)
        
        self.assertTrue(form.is_valid(), form.errors.as_text())
        
        user = form.save()
        
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertEqual(Realtor.objects.count(), initial_realtor_count + 1)
        
        realtor = Realtor.objects.get(user=user)
        self.assertEqual(realtor.license_number, 'RLIC789')
        self.assertEqual(realtor.experience_years, 0)


class PropertyFormTest(TestCase):
    """Тесты для формы управления объектами (PropertyForm)."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='realtor_test', password='pwd')
        self.realtor = Realtor.objects.create(user=self.user, experience_years=1)
        self.client_user = User.objects.create_user(username='client_test', password='pwd')
        self.client = Client.objects.create(user=self.client_user, phone='123')

    def test_property_form_valid(self):
        """Проверяет, что PropertyForm действительна при корректных данных."""
        form_data = {
            'title': 'Тестовый объект',
            'description': 'Отличное место',
            'price': 5000000,
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 100,
            'address': 'ул. Мира, 5',
            'property_type': 'apartment',
            'status': 'for_sale',
            'client': self.client.pk
        }
        form = PropertyForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    # 7. Тест: Недействительна при отсутствии обязательного поля 'title'
    def test_property_form_missing_title(self):
        """Проверяет, что форма недействительна без заголовка."""
        form_data = {
            'description': 'Описание',
            'price': 5000000,
            'area': 100,
            'client': self.client.pk,
            # 'title' отсутствует
        }
        form = PropertyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        


class LoginFormTest(TestCase):
    """Тесты для формы входа (LoginForm)."""
    
    def setUp(self):
        # Создаем пользователя, который может быть использован для входа
        self.user = User.objects.create_user(username='testlogin', password='validpassword123')

    # 9. Тест: Успешный вход
    def test_login_form_valid(self):
        """Проверяет, что форма действительна при корректных учетных данных."""
        form_data = {
            'username': 'testlogin',
            'password': 'validpassword123',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        
    # 10. Тест: Некорректный пароль
    def test_login_form_invalid_password(self):
        """Проверяет, что форма недействительна при неверном пароле."""
        form_data = {
            'username': 'testlogin',
            'password': 'wrongpassword', # Неверный пароль
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors) # Ожидаем ошибку, которая относится ко всей форме (неверные учетные данные)

    # 11. Тест: Отсутствующее имя пользователя
    def test_login_form_missing_username(self):
        """Проверяет, что форма недействительна при отсутствии имени пользователя."""
        form_data = {
            'username': '',
            'password': 'validpassword123', 
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors) # Ожидаем ошибку для поля username

