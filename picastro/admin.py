from django.contrib import admin

from .models import Post, StarCamp, Equipment, Imageissaved, Subscription, UserProfile

admin.site.register(Post)
admin.site.register(StarCamp)
admin.site.register(UserProfile)
admin.site.register(Equipment)
admin.site.register(Imageissaved)
admin.site.register(Subscription)


