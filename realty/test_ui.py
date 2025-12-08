from django.test import TestCase, Client
from django.urls import reverse

class HomeViewTest(TestCase):
    def test_link_to_property_list_exists(self):
        client = Client()
        response = client.get(reverse('home'))
        # Проверяем, что на странице есть ссылка на 'property_list'
        self.assertContains(response, f'href="{reverse("property_list")}"')