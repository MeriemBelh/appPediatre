"""AppPediatre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', include('testExample.urls')),
    path('', views.index, name='homPage'),
    #path('',views.header),
    path('pediatre/', include('Pediatre.urls'), name='pediatre'),
    path('patient/', include('Patient.urls'), name='patient'),
    path('administrateur/', include('Administrateur.urls'), name='administrateur'),
    path('login/', views.loginUsers, name='loginUsers'),
    path('media/images/', views.image, name='image'),
    path('media/videos/', views.video, name='video'),
    path('about/', views.about, name='about'),
    path('actualites/', views.actualites, name='actualites'),
    path('actualite/<int:actualite_id>/', views.actualite, name='actualite'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)