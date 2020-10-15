from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_views),
    path('/team/<str:team_name>', team),
    path('/update_profiles', update_profile),
]
