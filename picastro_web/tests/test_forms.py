from django.test import SimpleTestCase, TestCase
from tempfile import NamedTemporaryFile

from picastro_web.forms import LoginForm, UserRegistrationForm, PostForm
from picastro.tests.test_setup import TestSetup
from picastro.models import StarCamp


class TestLoginForm(SimpleTestCase):

    def test_valid_data(self):
        form = LoginForm(data={
            "username": "testusername",
            "password": "testpassword"
        })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestUserRegistrationForm(TestCase):

    def test_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testusername',
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
            'email': 'test@email.com',
            'password': 'test_password',
            'password2': 'test_password'
        })
        
        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = UserRegistrationForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)


class TestPostForm(TestSetup):

    def test_valid_data(self):
        form = PostForm(data=self.post_data)
        print(form.errors)

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 10)
