from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_views),
    path('/update_profiles', update_profile)

]
