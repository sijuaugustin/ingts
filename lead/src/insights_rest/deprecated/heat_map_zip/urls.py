from django.conf.urls import url, include
from .views import zip_api
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'zip', zip_api, 'zip_api')

urlpatterns = [
    url(r'^', include(router.urls)),
]
