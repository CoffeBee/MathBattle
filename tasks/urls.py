from django.urls import path
from .views import *

urlpatterns = [
    path('/<str:task_title>/', task),
]