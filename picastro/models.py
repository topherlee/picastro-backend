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