from django.urls import path
from .views import *

urlpatterns = [
    path('/<str:theme_name>/<str:task_title>/', task)
]