from django.contrib import admin

from .models import Post, StarCamp, Equipment, SavedImages, Subscription, UserProfile, Comment

admin.site.register(Post)
admin.site.register(StarCamp)
admin.site.register(UserProfile)
admin.site.register(Equipment)
admin.site.register(SavedImages)
admin.site.register(Subscription)
admin.site.register(Comment)
