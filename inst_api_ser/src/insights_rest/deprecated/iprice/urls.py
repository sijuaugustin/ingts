'''
Created on Mar 16, 2016

@author: joseph
'''
from django.conf.urls import url, include
from .views import iPriceTrendViewSet, get_name
from rest_framework import routers
# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'is_staff')
# 
# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# 
# # Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'trend', iPriceTrendViewSet, 'iPriceTrendViewSet')
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ui', get_name)
]