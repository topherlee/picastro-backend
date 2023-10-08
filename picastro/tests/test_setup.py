from rest_framework.test import APITestCase
from django.urls import reverse
from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

from picastro.models import StarCamp, Post, PicastroUser, Equipment, SavedImages

from picastro.models import StarCamp


class TestSetup(APITestCase):

    def setUp(self):
        
        self.register_url = reverse('auth_user_create')
        self.login_url = reverse('auth_login')
        self.current_user_url = reverse('auth_user_current')
        self.posts_url = reverse('feed_of_posts')
        self.post_details_url = reverse('update_delete_posts', args=[1])
        self.image_like_url = reverse('image_like', args=[1])

        self.user_data = {
            "username": "username",
            "password": "password123",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@picastro.com"
        }

        self.login_data = {
            "username": "username",
            "password": "password123"
        }
        
        self.user_profile_data = {
            "location": "Dundee_test",
            "userDescription": "long test description",
            "genderIdentifier": "diverse",
        }

        self.post_data = {
            #"image": SimpleUploadedFile('small.gif', self.small_gif, content_type='image/gif'),
            "astroNameShort": "IC442",
            "astroName": "Star #1",
            "exposureTime": "6 hrs",
            "moonPhase": "50%",
            "cloudCoverage": "10%",
            "bortle": "3",
            "imageDescription": "The Omega Nebula",
            "imageCategory": "nebula",
            "poster": "1",
        }

        self.starcamp_data1 = {
            "starCampName": "Aberdeen",
            "starCampLocation": "Aberdeen"
        }

        self.starcamp_data2 = {
            "starCampName": "Glasgow",
            "starCampLocation": "Glasgow"
        }

        self.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        return super().setUp()

    def create_test_user(self):
        user = PicastroUser.objects.create_user(
            username = "username",
            password = "password123",
            first_name = "test_first",
            last_name = "test_last",
            email = "test@picastro.com", 
        )
        return user

    def create_test_starcamp(self):
        starcamp = StarCamp.objects.create(
            starCampName = "Aberdeen",
            starCampLocation = "Aberdeen"
        )
        return starcamp
    
    def create_test_post(self, user):
        post = Post.objects.create(
            # image = NamedTemporaryFile(suffix='.jpg', prefix="test_img_"),
            # image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg'),
            image = SimpleUploadedFile('small.gif', self.small_gif, content_type='image/gif'),
            astroNameShort = "IC442",
            astroName = "Star #1",
            exposureTime = "6 hrs",
            moonPhase = "50%",
            cloudCoverage = "10%",
            bortle = "3",
            imageDescription = "The Omega Nebula",
            imageCategory = "nebula",
            poster = user,
        )
        return post
    
    def create_test_equipment(self, user):
        equipment = Equipment.objects.create(
            setName = "Test setName",
            telescopeName = "Test TelescopeName",
            cameraName = "Test cameraName",
            guideCameraName = "Test guideCameraName",
            offAxisguidecamera = "Test offAxisguidecamera",
            filterWheelName = "Test filterWheelName",
            filters = "Test Filters",
            barlowLense = "Test BarlowLense",
            otherEquipment = "Test otherEquipment",
            userId = user
        )
        return equipment

    def create_test_saved_image(self, user, post):
        saved_image = SavedImages.objects.create(
            user = user,
            post = post
        )
        return saved_image

    def tearDown(self):
        return super().tearDown()
