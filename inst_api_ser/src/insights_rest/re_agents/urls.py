from django.conf.urls import url, include
from rest_framework import routers
from .views import AgentDetails


router = routers.DefaultRouter()
router.register(r'details', AgentDetails, 'AgentDetails')


urlpatterns = [
    url(r'^', include(router.urls)),
]
