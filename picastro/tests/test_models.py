import pytest
from django.test import TestCase

from picastro.models import Post
from picastro.tests.test_setup import TestSetup

pytestmark = pytest.mark.django_db


# class TestPostModel(TestSetup):
#     def test_output_string_method(self, post_factory):
#         #Arrange
#         #Act
#         post_data = post_factory()
#         #Assert
#         assert post_data.__str__() == "username - 2023-04-05 12:06:09.920441"


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