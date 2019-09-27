from django.urls import path
from .views import *

urlpatterns = [
    path('/<int:task_id>/', task)
]