from django.contrib import admin

# Register your models here.
from .models import Commits,UserProfileInfo, User

admin.site.register(Commits)
admin.site.register(UserProfileInfo)