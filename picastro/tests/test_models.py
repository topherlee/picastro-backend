import pytest
from django.test import TestCase
from django.contrib.auth.models import User

from picastro.models import Post
from picastro.tests.test_setup import TestSetup

pytestmark = pytest.mark.django_db


class TestPostModel(TestSetup):

    def test_should_create_post(self):
        self.assertEqual(User.objects.count(), 0)
        post = self.create_test_post()
        self.assertEqual(User.objects.count(), 1)

    def test_output_string_method(self):
        #Arrange
        #Act
        post = self.create_test_post()
        #Assert
        assert post.__str__() == "username - 2023-04-05 12:06:09.920441"


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


# class TestStarCampModel(TestSetup):
#     def test_output_string_method(self, starcamp_factory):
#         #Arrange
#         #Act
#         starcamp_data = starcamp_factory()
#         #Assert
#         assert starcamp_data.__str__() == "Aberdeeen"


# class TestUserProfileModel:
#     def test_output_string_method():
#         #Arrange
#         #Act
#         #Assert
#         pass


# class TestEquipmentModel:
#     def test_output_string_method():
#         #Arrange
#         #Act
#         #Assert
#         pass


# class TestSavedImagesModel:
#     def test_output_string_method():
#         #Arrange
#         #Act
#         #Assert
#         pass


# class TestSubscriptionModel:
#     def test_output_string_method():
#         #Arrange
#         #Act
#         #Assert
#         pass