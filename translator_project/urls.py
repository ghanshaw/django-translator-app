"""translator_project URL Configuration"""


from django.conf.urls import *
from django.contrib import admin

from translate.views import base

from rest_framework import routers
from translate.views import TranslationViewSet, LanguageViewSet

router = routers.DefaultRouter()
router.register(r'translate', TranslationViewSet) # Includes GET/POST/DELETE for individual translate and multiple translates
router.register(r'languages', LanguageViewSet, base_name='supported_languages')


urlpatterns = [
    url(r'^$', base),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls))
]
