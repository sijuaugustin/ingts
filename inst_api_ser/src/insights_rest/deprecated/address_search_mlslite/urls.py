from django.conf.urls import url, include
from .views import address_search
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'radius_search', address_search, 'address_search')

urlpatterns = [
    url(r'^', include(router.urls)),
]
