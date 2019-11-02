from django.urls import path
from .views import *

urlpatterns = [
    path('theme/', themes),
    path('contest/', contests),
    path('contest/<str:contest_name>', contest),
    path('theme/<str:theme_name>/', theme),
    path('solutions/', solutions),
    path('solutions/<int:submit_id>', solution),

]
