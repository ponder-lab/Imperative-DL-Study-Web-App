from django.contrib import admin

# Register your models here.
from .models import Commits, User

admin.site.register(Commits)