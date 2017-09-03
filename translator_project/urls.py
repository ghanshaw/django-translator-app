"""translator_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin

from translate.views import input
from translate.views import result
from translate.views import base

# from django.config.urls import *
from rest_framework import routers
from translate.views import TranslationViewSet, LanguageViewSet
# from movie import views

router = routers.DefaultRouter()
router.register(r'translate', TranslationViewSet) # Includes GET/POST/DELETE for individual translate and multiple translates
router.register(r'languages', LanguageViewSet, base_name='supported_languages')


urlpatterns = [
    url(r'^$', base),
    # url(r'^result/', result),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls))
]
