from django.urls import path
from .views import *

urlpatterns = [
    path('theme/', themes),
    path('contest/', contests),
    path('contest/<str:contest_name>', contest),
    path('theme/<str:theme_name>/', theme),
    path('solutions/', solutions),
    path('solutionspage/<int:page>', solutionspage),
    path('solutions/<int:submit_id>', solution),
    path('about/', main)
]
