import json
import datetime
from multiprocessing.sharedctypes import Value
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from picastro.models import (
    Post,
    StarCamp,
    User,
    UserProfile,
    Equipment,
    Imageissaved,
    Subscription,
    savedImages
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        #drop all tables to preven duplicates
        Post.objects.all().delete()
        Post.objects.all().delete()
        StarCamp.objects.all().delete()
        UserProfile.objects.all().delete()
        Equipment.objects.all().delete()
        Imageissaved.objects.all().delete()
        Subscription.objects.all().delete()
        print("Tables dropped succesfully")
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        with open(f'{base_dir}/picastro/data/homeFeed.json', 'r') as file:
            print("Json file opened successfully.")
            json_data = json.load(file)
            #print(json_data)
            for data_object in json_data:
                #print(data_object)
                post = Post.objects.create(
                    imageURL = data_object["imageURL"],
                    imageDescription = data_object["imageDescription"],
                    astroNameShort = data_object["astroNameShort"],
                    astroName = data_object["astroName"],
                    imageIsSaved = data_object["imageIsSaved"],
                    award = data_object["award"],
                    exposureTime = data_object["exposureTime"],
                    moonPhase = data_object["moonPhase"],
                    cloudCoverage = data_object["cloudCoverage"],
                    bortle = data_object["bortle"],
                    starCamp = data_object["starCamp"],
                    leadingLight = data_object["leadingLight"],
                    pub_date = datetime.now,
                    poster = ""???
                )
                post.save()

                star_camp = StarCamp.objects.create(
                    starCampName = data_object["starCamp"],
                    starCampLocation = data_object["starCamp"],
                )
                star_camp.save()

                user_profile = UserProfile.objects.create(
                    user = "",???
                    location = data_object["userLocation"],
                    starCampId = ""???,
                    subcriptionsExpiry = datetime.now + 2592000,
                    isEmailVerified = data_object["isEmailVerified"],
                    userDescription = data_object["userDescription"]
                )
                user_profile.save()

                if data_object["imageIsSaved"]:
                    saved_image = savedImages.objects.create(
                        userId = ""???,
                        imageId = ""???
                    )

                print(data_object["imageURL"])

