"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from vision import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Paths
    path('home/', views.something),
    path('upload/', views.upload_image, name='upload'),
    path('feedback/', views.feedback, name='feedback'),
    path('model/', views.arrange_model, name='arrange_model'),
    path('start-process/', views.start_process, name='start_process'),
    path('get-progress/', views.get_progress, name='get_progress'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
