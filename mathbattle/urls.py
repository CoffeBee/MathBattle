from django.contrib import admin
from django.urls import path,include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contest/', include('contest.urls')),
    path('', index),
    path('auth/', include('authorization.urls')),
    path('task', include('task.urls')),
    path('contest_page', include('contest_page.urls')),
    path('archiv/', include('archiv.urls')),
    path('userprofile', include('userprofile.urls'))
]
