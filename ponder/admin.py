from django.contrib import admin

# Register your models here.
from .models import Commits

admin.site.register(Commits)