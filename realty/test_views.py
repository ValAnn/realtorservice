from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Property, Realtor

User = get_user_model() 

class PublicViewsTest(TestCase):
    """Тесты для публичных представлений (home, list, detail)."""
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.list_url = reverse('property_list')
        
        self.user = User.objects.create_user(username='test_realtor', password='password')
        self.realtor = Realtor.objects.create(user=self.user, experience_years=3)
        self.property1 = Property.objects.create(
            title='Тестовый Объект', price=10000000, realtor=self.realtor, status='for_sale'
        )
        self.detail_url = reverse('property_detail', kwargs={'pk': self.property1.pk})

    # 16. Тест: Статус-код главной страницы
    def test_home_page_status_code(self):
        """Проверяет, что главная страница загружается успешно (200)."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    # 17. Тест: Контекст главной страницы
    def test_home_page_context_data(self):
        """Проверяет, что в контексте главной страницы переданы риелторы."""
        response = self.client.get(self.home_url)
        self.assertIn('realtors', response.context)
        self.assertEqual(len(response.context['realtors']), 1)
        
    # 18. Тест: Статус-код списка объектов
    def test_property_list_status_code(self):
        """Проверяет, что страница списка объектов загружается успешно (200)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        
    # 19. Тест: Статус-код детальной страницы (существующий)
    def test_property_detail_existing_object(self):
        """Проверяет, что детальная страница существующего объекта возвращает 200."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    # 20. Тест: Статус-код детальной страницы (несуществующий)
    def test_property_detail_non_existing_object(self):
        """Проверяет, что детальная страница несуществующего объекта возвращает 404."""
        non_existent_url = reverse('property_detail', kwargs={'pk': 9999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, 404)