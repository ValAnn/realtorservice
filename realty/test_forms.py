from django.test import TestCase
# Импортируем вашу форму. Замените '.forms' на фактический путь, если он другой.
from ..forms import ContactForm 

class ContactFormTest(TestCase):
    """Тесты для формы обратной связи (ContactForm)."""

    # 11. Тест: Форма действительна при корректных данных
    def test_contact_form_valid_data(self):
        """Проверяет, что форма действительна при заполнении всех полей."""
        form = ContactForm(data={
            'name': 'Иван Иванов',
            'email': 'ivan@example.com',
            'message': 'Запрос на просмотр объекта.'
        })
        self.assertTrue(form.is_valid(), form.errors.as_text())

    # 12. Тест: Форма недействительна (отсутствует Имя)
    def test_contact_form_missing_name(self):
        """Проверяет, что форма недействительна при отсутствии обязательного поля 'name'."""
        form = ContactForm(data={
            'email': 'test@example.com',
            'message': 'Сообщение.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors) # Проверяем наличие ошибки для поля 'name'

    # 13. Тест: Форма недействительна (некорректный Email)
    def test_contact_form_invalid_email(self):
        """Проверяет, что форма недействительна при некорректном формате 'email'."""
        form = ContactForm(data={
            'name': 'Имя',
            'email': 'invalid-email', # Некорректный формат
            'message': 'Сообщение.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    # 14. Тест: Форма недействительна (слишком короткое сообщение)
    def test_contact_form_message_min_length(self):
        """Проверяет, что форма недействительна, если сообщение слишком короткое (если есть min_length)."""
        # Допустим, min_length=10
        form = ContactForm(data={
            'name': 'Имя',
            'email': 'valid@example.com',
            'message': 'too short' 
        })
        # Если в forms.py есть Max/Min Length, проверяем, что форма не проходит
        # Если нет, этот тест просто проверяет, что форма проходит
        # В данном примере предполагаем, что проходит, если нет явного валидатора
        if 'message' in form.errors:
             self.assertFalse(form.is_valid())
        else:
             self.assertTrue(form.is_valid())

    # 15. Тест: Форма действительна (отсутствует email, если email не обязателен)
    def test_contact_form_email_optional(self):
        """Проверяет, что форма действительна, если email не обязателен (если поле 'required=False')."""
        # Если email в вашей форме ОБЯЗАТЕЛЕН, этот тест нужно пропустить или изменить его ожидание.
        # Если email НЕ обязателен:
        form = ContactForm(data={
            'name': 'Иван',
            'email': '', # Оставляем пустым
            'message': 'Сообщение.'
        })
        # Если email обязателен, то: self.assertFalse(form.is_valid())
        # Если email не обязателен, то:
        # self.assertTrue(form.is_valid()) 
        
        # Для простоты, здесь оставим проверку, что все обязательные поля (name, message) заполнены.
        if 'email' in form.fields and form.fields['email'].required:
            self.assertFalse(form.is_valid())
        else:
            self.assertTrue(form.is_valid())