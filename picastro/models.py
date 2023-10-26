import os
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .managers import PicastroUserManager

#import uuid


class PicastroUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=16)
    isEmailVerified = models.BooleanField(default=False)
    isPhoneVerified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    subcriptionsExpiry = models.DateTimeField(auto_now_add=True)
    profileImage = models.ImageField(
        upload_to='profileImages/',
        default='profileImages/sampleuserbig.png',
        blank=True)
    location = models.CharField(max_length=50, blank=True)
    userDescription = models.TextField(default="", max_length=200, blank=True)
    genderIdentifier = models.TextField(default="divers", max_length=10, blank=True)

    objects = PicastroUserManager()

    def save(self, *args, **kwargs): 
        print("processing profile image", self.profileImage)
        image = Image.open(self.profileImage)
        image = ImageOps.exif_transpose(image)
        thumb_size = (500, 500)
        image.thumbnail(thumb_size, Image.LANCZOS)
        print("image writing")

        thumb_name, thumb_extension = os.path.splitext(self.profileImage.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = 'profile_image_' + self.username + thumb_extension
        print('Profile image will be saved as ' + thumb_filename)

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        elif thumb_extension in ['.tif', '.tiff']:
            FTYPE = 'TIF'
        else:
            return    # Unrecognized file type
        
        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.profileImage.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        super(PicastroUser, self).save(*args, **kwargs)


    def __str__(self):
        return self.username

class Post(models.Model):
    image = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='resize/', editable=False, default="")
    #thumbnail_xs = models.ImageField(upload_to='resize_xs/', editable=False, default="")
    #thumbnail_s = models.ImageField(upload_to='resize_s/', editable=False, default="")
    imageDescription = models.TextField(max_length=2000)
    imageCategory = models.TextField(default="others")
    astroNameShort = models.TextField(max_length=10)
    astroName = models.TextField(max_length=50)
    award = models.TextField(default='None')
    exposureTime = models.TextField(max_length=8)
    moonPhase = models.TextField(max_length=4)
    cloudCoverage = models.TextField(max_length=4)
    bortle = models.TextField(max_length=1)
    # leadingLight = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aspectRatio = models.FloatField(editable=False, default=1)

    # Class string added to store original name of photo
    original_image_name = None              # from https://stackoverflow.com/a/74696504

    def __str__(self):
        return f'{self.poster.username} - {str(self.pub_date)}'

    # When the form is initialized save the original photo name
    def __init__(self, *args, **kwargs):    # from https://stackoverflow.com/a/74696504
        super().__init__(*args, **kwargs)
        self.original_image_name = self.image.name

    def save(self, *args, **kwargs):        # from https://stackoverflow.com/a/74696504
        # This checks if the photo was updated or not before saving a thumbnail
        # print("original name", self.original_image_name)
        # print("image name", self.image.name)
        # #if self.original_image_name != self.image.name:
            
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail')
    
        super(Post, self).save(*args, **kwargs)

    def make_thumbnail(self):
        # image = Image.open(self.image)
        print("image processing", self.image)
        # im = Image(str(self.image)) # does not work with pgmagick
        # im.quality(100)
        # im.scale('1000x1000')
        # im.sharpen(1.0)
        # im.write(str(BASE_DIR / 'media/resize') + '/' + image_uri.split("/")[-1])

        image = Image.open(self.image)
        image = ImageOps.exif_transpose(image)  #reset width and height if the exif of an image has rotation on it
        self.aspectRatio = image.width / image.height
        # print(self.aspectRatio, image.width, image.height)
        thumb_size = (1000, 1000)
        image.thumbnail(thumb_size, Image.LANCZOS)
        print("image writing")

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        elif thumb_extension in ['.tif', '.tiff']:
            FTYPE = 'TIF'
        else:
            return False    # Unrecognized file type
        
        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


class StarCamp(models.Model):
    starCampName = models.TextField(unique=True)
    starCampLocation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.starCampName


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # image = models.ImageField(upload_to='user_images/')
#     # is_verified = models.BooleanField(default=False)
#     profileImage = models.ImageField(upload_to='profileImages/', default='profileImages/sampleuserbig.png')
#     location = models.CharField(max_length=50, blank=True)
#     starCampId = models.ForeignKey(StarCamp, on_delete=models.CASCADE, null=True, blank=True)
#     subcriptionsExpiry = models.DateTimeField(auto_now_add=True)
#     isEmailVerified = models.BooleanField(default=False)
#     userDescription = models.TextField(default="", max_length=200)
#     genderIdentifier = models.TextField(default="divers", max_length=10)

#     def __str__(self):
#         return self.user.username

#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             UserProfile.objects.create(
#             user=instance,
#         )


class Equipment(models.Model):
    setName = models.CharField(max_length=140, default='DEFAULT VALUE')
    telescopeName = models.TextField()
    cameraName = models.TextField()
    guideCameraName = models.TextField()
    offAxisguidecamera = models.TextField()
    filterWheelName = models.TextField()
    filters = models.TextField()
    barlowLense = models.TextField()
    otherEquipment = models.TextField()
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.setName
    

class SavedImages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {str(self.post.id)}'
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user', 'post'], name='unique_user_post_combination'
    #         )
    #     ]


# class Subscription(models.Model):
#     subscriptionsPlan = models.TextField()
#     subscriptionsDuration = models.DurationField()
#     subscriptionsPrice = models.DecimalField(max_digits=5, decimal_places=2)

#    def __str__(self):
#        return self.subcriptionsPlan


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return '%s - %s' % (self.commenter_name,self.comment_body)
