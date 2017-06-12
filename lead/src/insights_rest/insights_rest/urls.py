
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

# """ DEPRECATED """
import deprecated.iprice_v1.urls as iprice_v1_urls
import deprecated.iprice_v2.urls as iprice_v2_urls
import deprecated.heat_map_v1.urls as heatmap_v1_urls
import deprecated.heat_map_v2.urls as heatmap_v2_urls
import deprecated.rfm_bestfit_v1.urls as rfm_bestfit_v1_urls
import deprecated.agents_v1.urls as agents_v1_urls
import deprecated.rfm_v1.urls as rfm_v1_urls
import deprecated.heat_map_zip.urls as heatmap_zip_urls
import deprecated.address_search_mlslite.urls as address_search_mlslite_urls
import deprecated.iprice_v3.urls as iprice_v3_urls
# """ END DEPRECATED """

import agentsrfm.urls as agentsrfm_urls
import re_agents.urls as agents_urls
import iprice_mlslite.urls as iprice_mlslite_urls
import heatmap.urls as heatmap_urls
import lead.urls as lead_urls


from django.conf import settings
from django.conf.urls.static import static


# """ DEPRECTED """
internal_apis = [url(r'^iprice/v1/', include(iprice_v1_urls)),
                 url(r'^iprice/v2/', include(iprice_v2_urls)),
                 url(r'^rfm/bestfit/v1/', include(rfm_bestfit_v1_urls)),
                 url(r'^rfm/agents/v1/', include(agents_v1_urls)),
                 url(r'^rfm/topten/v1/', include(rfm_v1_urls)),
                 url(r'^mlslite_radius/', include(address_search_mlslite_urls)),
                 url(r'^heatmap/v1/', include(heatmap_v1_urls)),
                 url(r'^heatmap/v2/', include(heatmap_v2_urls)),
                 url(r'^heatmap/zip_v2/', include(heatmap_zip_urls)),
                 url(r'^iprice/v3/', include(iprice_v3_urls)),
                 url(r'^lead/', include(lead_urls)),
                 ]
# """ END DEPRECTED """

urlpatterns = [
    url(r'^', include(internal_apis, namespace="internal_apis")),
    url(r'^admin/', admin.site.urls),
    url(r'^iprice/mlslite/', include(iprice_mlslite_urls)),
    url(r'^rfm/agents/', include(agentsrfm_urls)),
    url(r'^rfm/agent/', include(agents_urls)),
    url(r'^heatmap/', include(heatmap_urls)),
    url(r'^lead/', include(lead_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^accounts/login/$', auth_views.login, name='login'),
] + (static(settings.TEST_REPORTS_URL, document_root=settings.REPORT_ROOT) if hasattr(settings, 'TEST_REPORTS_URL') else [])
