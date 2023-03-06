from django.contrib import admin

from .models import Post, StarCamp, Equipment, savedImages, Subscription, UserProfile

admin.site.register(Post)
admin.site.register(StarCamp)
admin.site.register(UserProfile)
admin.site.register(Equipment)
admin.site.register(savedImages)
admin.site.register(Subscription)


