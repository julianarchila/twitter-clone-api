"""config URL Configuration

"""

# Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# Django REST Framework
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("api.users.urls")),
    path("", include("api.tweets.urls")),
    path("docs/", include_docs_urls(title="TwittercloneAPI")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
