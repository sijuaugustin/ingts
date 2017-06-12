from django.conf.urls import url, include
from rest_framework import routers
from .views import Agent

router = routers.DefaultRouter()
router.register(r'Agent', Agent, 'Agnt')

urlpatterns = [
    url(r'^', include(router.urls)),
]
