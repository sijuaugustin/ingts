'''
Created on Dec 29, 2016

@author: joseph
'''
from django.conf.urls import url, include
from rest_framework import routers
from .views import HPIRawViewset
from .views import HPIPlaceNames
from .views import HPIYears
from .views import HPI3Zips
from .views import HPI3ZipYears
from .views import HPI3ZipRawData
from .views import HPIPriceTrendMix

router = routers.DefaultRouter()
router.register(r'data', HPIRawViewset, 'HPIRawViewset')
router.register(r'locations', HPIPlaceNames, 'HPIPlaceNames')
router.register(r'years', HPIYears, 'HPIYears')
router.register(r'3zipdata', HPI3ZipRawData, 'HPI3ZipRawData')
router.register(r'3zips', HPI3Zips, 'HPI3Zips')
router.register(r'3zipyears', HPI3ZipYears, 'HPI3ZipYears')
router.register(r'hpiipt', HPIPriceTrendMix, 'HPIPriceTrendMix')
urlpatterns = [url(r'^', include(router.urls))]
