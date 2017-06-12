"""DjangoRestDemo URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
import demo.urls
import reagents.urls
import pricing.urls
import marketgrowth.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^demo/', include(demo.urls)),
    url(r'^reagents/', include(reagents.urls)),
    url(r'^pricing/', include(pricing.urls)),
    url(r'^marketgrowth/', include(marketgrowth.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls'))

]
