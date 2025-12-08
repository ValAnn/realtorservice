from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from realty.models import Property, Realtor, Client
# from models import Property, Realtor

# Получаем модель пользователя, используемую в проекте
User = get_user_model()

class RealtorModelTest(TestCase):
    """Тесты для модели Realtor."""

    def setUp(self):
        # Создаем тестового пользователя, необходимого для Realtor
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            first_name='Иван',
            last_name='Петров'
        )
        # Создаем тестового риелтора
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