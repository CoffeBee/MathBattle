from django.urls import path
from .views import *

urlpatterns = [
    path('/<int:contest_id>/', contest)
]