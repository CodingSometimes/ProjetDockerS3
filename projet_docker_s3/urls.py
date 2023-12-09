
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # admin
    path('blog/', include('blog.urls')),  # blog
    path('auth/', include('authentication.urls')),  # blog
]
