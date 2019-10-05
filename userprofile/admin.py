from django.contrib import admin
from .models import Profile, Rang, UserRang

admin.site.register(Profile)
admin.site.register(Rang)
admin.site.register(UserRang)
