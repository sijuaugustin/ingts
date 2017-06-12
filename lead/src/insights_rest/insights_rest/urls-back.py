"""iInsights URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
# from django.conf.urls import url, include
# from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
import iCms.urls
import iCma_test.urls
import iPrice.urls
import iPrice_v1.urls
import iPrice_v2.urls
import iPrice_v3.urls
import heat.urls
import heat_v1.urls
import heat_v2.urls
import RfmBestfitAPI.urls
import AgentsApi.urls
import RfmApi.urls
import HeatMap_API_ZIP.urls
import Address_Search_MLSLite.urls
import RfmBestfitAPI_v2.urls
import AgentsApi_v2.urls
import RfmApi_v2.urls
import iPrice_mlslite.urls



# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^icma/', include(iCms.urls)),
    url(r'^iprice/', include(iPrice.urls)),
    url(r'^iprice/v1/', include(iPrice_v1.urls)),
    url(r'^iprice/v2/', include(iPrice_v2.urls)),
    url(r'^iprice/v3/', include(iPrice_v3.urls)),
    url(r'^iprice/mlslite/', include(iPrice_mlslite.urls)),
    url(r'^icma/test/', include(iCma_test.urls)),
    url(r'^heatmap/', include(heat.urls)),
    url(r'^heatmap/v1/', include(heat_v1.urls)),
    url(r'^heatmap/v2/', include(heat_v2.urls)),
	url(r'^rfm/bestfit/v1/', include(RfmBestfitAPI.urls)),
	url(r'^rfm/Agents/v1/', include(AgentsApi.urls)),
	url(r'^rfm/topten/v1/', include(RfmApi.urls)),
	url(r'^heatmap/zip_v2/', include(HeatMap_API_ZIP.urls)),
    url(r'^MLSLite_radius/', include(Address_Search_MLSLite.urls)),
    url(r'^rfm/bestfit/v2/', include(RfmBestfitAPI_v2.urls)),
    url(r'^rfm/Agents/v2/', include(AgentsApi_v2.urls)),
    url(r'^rfm/topten/v2/', include(RfmApi_v2.urls)),
	
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]



