"""
URL configuration for dj_class_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path

from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from posts.views.auth_views import login_view, staff_login_view, logout_view, login_or_create_user

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('login/', login_view, name='login'),
    path('staff/login/', staff_login_view, name='staff_login'),
    path("staff/", include("posts.staff_urls")),
    path('logout', logout_view, name="logout"),
    path("guest-login/", login_or_create_user, name="guest-login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)