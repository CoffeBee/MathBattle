from django.urls import path
from .views import *

urlpatterns = [
    path('', themes),
    path('<str:theme_name>/', theme)

]
