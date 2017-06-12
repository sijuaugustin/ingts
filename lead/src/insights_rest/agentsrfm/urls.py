from django.conf.urls import url, include
from .views import BestFitAgent, Top10Agents
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'bestfit', BestFitAgent, 'BestFitAgent')
router.register(r'topten', Top10Agents, 'Top10Agents')

urlpatterns = [
    url(r'^', include(router.urls)),
]
