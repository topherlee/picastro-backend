# from tempfile import NamedTemporaryFile

# from factory.django import DjangoModelFactory
# from django.contrib.auth.models import User

# from picastro.models import (
#     Equipment,
#     Post,
#     SavedImages,
#     StarCamp,
#     Subscription,
#     UserProfile
# )


# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = User

#     username: "username"
#     password: "password123"
#     first_name: "test_first"
#     last_name: "test_last"
#     email: "test@picastro.com"
#     location: "Dundee_test"
#     userDescription: "long test description"
#     genderIdentifier: "diverse"


# class PostFactory(DjangoModelFactory):
#     class Meta:
#         model = Post
    
#     # def create_test_image():
#     #     image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
#     #     image_file = NamedTemporaryFile(suffix='.png')
#     #     #image.save(image_file)
#     #     return image_file
    
#     # test_image = create_test_image()

#     image = NamedTemporaryFile(suffix='.jpg', prefix="test_img_")
#     thumbnail = "1_thumb" 
#     imageDescription = "I have taken this splendid picture"
#     imageCategory = "nebula"
#     astroNameShort = "NGC 1-Test"
#     astroName = "NGC 1-Test Test Galaxy"
#     imageIsSaved = False
#     award = None
#     exposureTime = "1 hrs"
#     moonPhase = "10%"
#     cloudCoverage = "20%"
#     bortle = "5"
#     starCamp = factory.SubFactory(StarCampFactory)
#     # leadingLight = False
#     pub_date = "2023-04-05 12:06:09.920441"
#     poster = factory.SubFactory(UserFactory)

    
# class StarCampFactory(DjangoModelFactory):
#     class Meta:
#         model = StarCamp

#         starCampName = "Aberdeen"
#         starCampLocation = "Aberdeen"
    