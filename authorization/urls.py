from .views import *
from django.urls import path

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('signup/', register_view),
]
