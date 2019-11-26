from django.contrib import admin
from django.urls import path,include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('themes/', include('contest.urls')),
    path('', index),
    path('auth/', include('authorization.urls')),
    path('tasks', include('tasks.urls')),
    path('archiv/', include('archiv.urls')),
    path('userprofile', include('userprofile.urls')),
    path('summernote/', include('django_summernote.urls')),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
