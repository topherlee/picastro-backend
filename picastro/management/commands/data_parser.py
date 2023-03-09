import json
from datetime import datetime, timedelta
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
    Subscription,
    savedImages,
    ImageIsSaved
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        def drop_tables():
            #drop all tables to preven duplicates
            User.objects.all().delete()
            try:
                User.objects.all().delete()
            except:
                pass
            try:
                Post.objects.all().delete()
            except:
                pass
            try:
                StarCamp.objects.all().delete()
            except:
                pass
            try:
                UserProfile.objects.all().delete()
            except:
                pass
            try:
                Equipment.objects.all().delete()
            except:
                pass
            try:
                ImageIsSaved.objects.all().delete()
            except:
                pass
            try:
                Subscription.objects.all().delete()
            except:
                pass
            print("Tables dropped succesfully")
            
        drop_tables()
        
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        #create some users
        def create_users():
            print("started creating users")
            user = User.objects.create(
                username = "admin",
                first_name = "admin",
                last_name = "admin",
                email = "admin@picastro.com",
                password = "picastro",
                date_joined = datetime.now()
            )
            user.save()
            with open(f'{base_dir}/picastro/data/homeFeed.json', 'r') as file:
                print("Json file opened successfully.")
                json_data = json.load(file)
                #print(json_data)
                i = 0
                for data_object in json_data:
                    i += 1
                    print(i)
                    user_object = User.objects.filter(username = data_object["userName"])
                    if user_object.count() > 0:
                        continue
                    else:
                        first_name = "John" + str(i)
                        last_name = "Doe"
                        user = User.objects.create(
                            username = data_object["userName"],
                            first_name = first_name,
                            last_name = last_name,
                            email = first_name + last_name + "@picastro.com",
                            password = "picastro",
                            date_joined = datetime.now()
                        )
                        user.save()
                        print("user created", user)
                        
        
        create_users()


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
                    pub_date = datetime.now(),
                    poster = User.objects.get(username=data_object["userName"]),
                )
                post.save()

                try:
                    star_camp = StarCamp.objects.create(
                        starCampName = data_object["starCamp"],
                        starCampLocation = data_object["starCamp"],
                    )
                    star_camp.save()
                except IntegrityError:
                    pass


                if data_object.get("userDescription") != None:
                    userDescription = data_object["userDescription"]
                else:
                    userDescription = ""

                try:
                    user_profile = UserProfile.objects.create(
                        user = User.objects.get(username=data_object["userName"]),
                        location = data_object["userLocation"],
                        starCampId = StarCamp.objects.get(starCampName=data_object["starCamp"]),
                        subcriptionsExpiry = datetime.now() + timedelta(days=30),
                        isEmailVerified = True,
                        userDescription = userDescription
                    )
                    user_profile.save()
                except IntegrityError:
                    pass

                if data_object["imageIsSaved"]:
                    saved_image = savedImages.objects.create(
                        userId = User.objects.get(username=data_object["userName"]),
                        imageId = Post.objects.get(id=post.id),
                    )

                print(data_object["imageURL"])

