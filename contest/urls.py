from django.urls import path
from .views import *

urlpatterns = [
    path('theme/', themes),
    path('theme/<str:theme_name>/', theme),
    path('solutions/', solutions)

]
