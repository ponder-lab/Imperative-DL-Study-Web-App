from django.contrib import admin

# Register your models here.
from .models import Commit, User

admin.site.register(Commit)