from django.conf.urls import url, include
from .views import AgentsRFM
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'agents', AgentsRFM, 'AgentsRFM')

urlpatterns = [
    url(r'^', include(router.urls)),
]
