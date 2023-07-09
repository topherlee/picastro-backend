import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime

from picastro.models import Post, UserProfile
from picastro.tests.test_setup import TestSetup

pytestmark = pytest.mark.django_db


class TestPostModel(TestSetup):

    def test_should_create_post(self):
        self.assertEqual(Post.objects.count(), 0)
        user = self.create_test_user()
        post = self.create_test_post(user)
        self.assertEqual(Post.objects.count(), 1)

    def test_output_string_method(self):
        #Arrange
        #Act
        user = self.create_test_user()
        post = self.create_test_post(user)
        #Assert
        assert "username - " in post.__str__()


#     def test_init_method():
#         #Arrange
#         #Act
#         #Assert
#         pass


#     def test_save_method():
#         #Arrange
#         #Act
#         #Assert
#         pass


#     def test_make_thumbnail_method():
#         #Arrange
#         #Act
#         #Assert
#         pass


class TestStarCampModel(TestSetup):
    def test_output_string_method(self):
        #Arrange
        #Act
        starcamp = self.create_test_starcamp()
        #Assert
        assert starcamp.__str__() == "Aberdeen"


class TestUserProfileModel(TestSetup):

    def test_should_create_post(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
        post = self.create_test_user()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_output_string_method(self):
        #Arrange
        #Act
        user = self.create_test_user()
        #user_profile = self.create_test_user_profile()
        user_profile = UserProfile.objects.get(user=user)
        #Assert
        assert user_profile.__str__() == "username"


class TestEquipmentModel(TestSetup):

    def test_output_string_method(self):
        #Arrange
        #Act
        user = self.create_test_user()
        equipment = self.create_test_equipment(user=user)
        #Assert
        assert equipment.__str__() == "Test setName"


class TestSavedImagesModel(TestSetup):

    def test_output_string_method(self):
        #Arrange
        #Act
        user = self.create_test_user()
        post = self.create_test_post(user)
        saved_image = self.create_test_saved_image(user, post)
        #Assert
        assert saved_image.__str__() == "username - 1"


# class TestSubscriptionModel:
#     def test_output_string_method():
#         #Arrange
#         #Act
#         #Assert
#         pass