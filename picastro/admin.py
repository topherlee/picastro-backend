from django.contrib import admin

from .models import PicastroUser, Post, StarCamp, Equipment, SavedImages, Comment


class PicastroUserAdmin(admin.ModelAdmin):
    model = PicastroUser
    # fields = ["username", "email", "phone_no", 
    #           "profileImage", "first_name", "last_name", 
    #           "location", "userDescription", "genderIdentifier",
    #           "isEmailVerified", "isPhoneVerified",
    #           "is_active", "is_staff",
    #           "subscriptionExpiry", "payment_checkout_id"]
    readonly_fields = ["subscriptionExpiry"]


admin.site.register(PicastroUser, PicastroUserAdmin)
admin.site.register(Post)
admin.site.register(StarCamp)
#admin.site.register(UserProfile)
admin.site.register(Equipment)
admin.site.register(SavedImages)
#admin.site.register(Subscription)
admin.site.register(Comment)
