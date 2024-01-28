from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PicastroUser, Post, StarCamp, Equipment, SavedImages, Comment


class PicastroUserAdmin(UserAdmin):
    model = PicastroUser
    list_display = ["email", "username", "subcriptionsExpiry"]


admin.site.register(PicastroUser, )
admin.site.register(Post)
admin.site.register(StarCamp)
#admin.site.register(UserProfile)
admin.site.register(Equipment)
admin.site.register(SavedImages)
#admin.site.register(Subscription)
admin.site.register(Comment)
