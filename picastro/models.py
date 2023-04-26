from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
import os
from PIL import Image
from django.core.files.base import ContentFile


class Post(models.Model):
    image = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='resize/', editable=False, default="")
    imageDescription = models.TextField()
    imageCategory = models.TextField(default="others")
    astroNameShort = models.TextField()
    astroName = models.TextField()
    imageIsSaved = models.BooleanField(default=False)
    award = models.TextField(default='None')
    exposureTime = models.TextField()
    moonPhase = models.TextField()
    cloudCoverage = models.TextField()
    bortle = models.TextField()
    starCamp = models.TextField()
    # leadingLight = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

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
        thumb_size = (1000, 1000)
        image.thumbnail(thumb_size, Image.ANTIALIAS)
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # is_verified = models.BooleanField(default=False)
    profileImage = models.ImageField(upload_to='profileImages/', default='profileImages/sampleuserbig.png')
    location = models.CharField(max_length=100, blank=True)
    starCampId = models.ForeignKey(StarCamp, on_delete=models.CASCADE)
    subcriptionsExpiry = models.DateTimeField(auto_now_add=True)
    isEmailVerified = models.BooleanField()
    userDescription = models.TextField()
    genderIdentifier = models.TextField(default="divers")
   
    def __str__(self):
        return self.user.username


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
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.setName
    

class SavedImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {str(self.post.id)}'


class Subscription(models.Model):
    subscriptionsPlan = models.TextField()
    subscriptionsDuration = models.DurationField()
    subscriptionsPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.subcriptionsPlan
