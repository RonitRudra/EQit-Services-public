from django.contrib import admin
from .models import CustomUser, UserProfile, Interests, Friends
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Interests)
admin.site.register(Friends)