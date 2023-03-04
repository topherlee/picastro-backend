from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    #imageURL = models.URLField()
    imageURL = models.TextField()
    imageDescription = models.TextField()
    astroNameShort = models.TextField()
    astroName = models.TextField()
    imageIsSaved = models.BooleanField()
    award = models.TextField()
    exposureTime = models.TextField()
    moonPhase = models.TextField()
    cloudCoverage = models.TextField()
    bortle = models.TextField()
    starCamp = models.TextField()
    leadingLight = models.BooleanField()
    pub_date = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.poster.username

class StarCamp(models.Model):
    starCampName = models.TextField()
    starCamplocation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.starCampName

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    starCampId = models.ForeignKey(StarCamp, on_delete=models.CASCADE)
    subcriptionsExpiry = models.DateTimeField(auto_now_add=True)
    isEmailVerified = models.BooleanField()
    userDescription = models.TextField()
   
    def __str__(self):
        return self.user.username

class Equipment(models.Model):
    setName = models.TextField()
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
    

class Imageissaved(models.Model):
    userId= models.ForeignKey(User, on_delete=models.CASCADE)
    imageIsSaved = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.imageIsSaved

class Subscription(models.Model):
    subcriptionsPlan = models.TextField()
    subcriptionsDuration = models.DurationField()
    subcriptionsPrice = models.DecimalField(max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.subcriptionsPlan