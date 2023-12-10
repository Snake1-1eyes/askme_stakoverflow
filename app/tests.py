from django.test import TestCase
from django.urls import reverse
from django.core.paginator import Page
from django.contrib.auth.models import User

# Create your tests here.
from .forms import RegisterForm, EditProfileForm, NewQuestionForm, NewAnswerForm


# Тесты для forms
class RegisterFormTest(TestCase):

    def test_password_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'password')

    def test_repeat_password_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['repeat_password'].label == None or form.fields['repeat_password'].label == 'repeat_password')

    def test_first_name_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'Nick Name')

    def test_username_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'Login')

    def test_valid_form(self):
        data = {
            'username': 'testuser',
            'password': 'strongpassword_123',
            'first_name': 'Test',
            'email': 'test@example.com',
            'repeat_password': 'strongpassword_123',
            'avatar': None  # или используйте объект File, если хотите загрузить изображение
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        data = {
            'username': 'testuser',
            'password': 'weak12',
            'first_name': 'Test',
            'email': 'test@example.com',
            'repeat_password': 'weak',
            'avatar': None
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['Password must contain @/./+/-/_/&/*'])

    def test_invalid_username(self):
        data = {
            'username': 'user!name',
            'password': 'strongpassword123',
            'first_name': 'Test',
            'email': 'test@example.com',
            'repeat_password': 'strongpassword123',
            'avatar': None
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Login does not meet the requirements'])

    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password': 'strongpassword123',
            'first_name': 'Test',
            'email': 'test@example.com',
            'repeat_password': 'strongpassword124',
            'avatar': None
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Passwords do not match!'])


class EditProfileFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'avatar': None  # или объект File, если вы тестируете загрузку изображения
        }
        form = EditProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        form_data = {
            'username': 'very_long_username_that_exceeds_maximum_length_allowed_for_username',
            'email': 'test@example.com',
            'first_name': 'Test',
            'avatar': None
        }
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Login does not meet the requirements'])

    def test_missing_email(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'avatar': None
        }
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])


class NewQuestionFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'head': 'A valid question title',
            'body': 'A valid question body that exceeds the minimum length',
            'tags': 'tag1,tag2,tag3'  # теги разделены запятой
        }
        form = NewQuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_title(self):
        form_data = {
           'head': 'short',  # менее 10 символов
           'body': 'A valid question body that exceeds the minimum length',
           'tags': 'tag1,tag2,tag3'
        }
        form = NewQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['head'], ['Ensure this value has at least 10 characters (it has 5).'])

    def test_invalid_body(self):
        form_data = {
            'head': 'A valid question title',
            'body': 'short',  # менее 40 символов
            'tags': 'tag1,tag2,tag3'
        }
        form = NewQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['body'], ['Ensure this value has at least 40 characters (it has 5).'])

    def test_invalid_tags(self):
        form_data = {
            'head': 'A valid question title',
            'body': 'A valid question body that exceeds the minimum length',
            'tags': 'in*va,lid_tag'  # теги содержат запрещенные символы
        }
        form = NewQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['tags'], ['List of tags does not meet the requirements'])


class NewAnswerFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'body': 'A valid answer body that exceeds the minimum length'
        }
        form = NewAnswerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_body(self):
        form_data = {
           'body': 's',  # менее 2 символов
        }
        form = NewAnswerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['body'], ['Ensure this value has at least 2 characters (it has 1).'])


# Тесты для views
class YourViewTests(TestCase):

    def test_login_view_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница открывается успешно
        self.assertTemplateUsed(response, 'login.html')  # Проверяем, что используется правильный шаблон

    def test_login_view_POST_valid_data(self):
        user = User.objects.create_user(username='testuser', password='12345')  # Создаем пользователя для входа
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Проверяем, что после входа происходит редирект

    def test_login_view_POST_invalid_data(self):
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Проверяем, что при неверных данных отображается форма входа
        self.assertContains(response, 'Wrong password or user does not exist.')  # Проверяем, что отображается сообщение об ошибке

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Проверяем, что после выхода происходит редирект

    def test_signup_view_GET(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница открывается успешно
        self.assertTemplateUsed(response, 'signup.html')  # Проверяем, что используется правильный шаблон


    def test_setting_view_GET_logged_in(self):
        user = User.objects.create_user(username='testuser', password='12345')  # Создаем пользователя для входа
        self.client.force_login(user)
        response = self.client.get(reverse('setting'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница открывается успешно
        self.assertTemplateUsed(response, 'setting.html')  # Проверяем, что используется правильный шаблон

    def test_setting_view_POST_logged_in_valid_data(self):
        user = User.objects.create_user(username='testuser', password='12345')  # Создаем пользователя для входа
        self.client.force_login(user)
        response = self.client.post(reverse('setting'), {'first_name': 'Test'}, follow=True)
        self.assertEqual(response.status_code, 200)  # Проверяем, что данные успешно отправляются

    def test_ask_view_POST_valid_data(self):
        user = User.objects.create_user(username='testuser', password='12345')  # Создаем пользователя для входа
        self.client.force_login(user)
        response = self.client.post(reverse('ask'), {'head': 'Test Title', 'body': 'Test Body'})
        self.assertEqual(response.status_code, 200)  # Проверяем, что данные успешно отправляются

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница открывается успешно
        self.assertTemplateUsed(response, 'index.html')  # Проверяем, что используется правильный шаблон

