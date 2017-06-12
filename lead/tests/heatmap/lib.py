'''
Created on Dec 16, 2016

@author: vishnu.sk
'''
import urlparse
import json
import requests


class HeatMapAPI():
    def __init__(self, host="https://insights.propmix.io:8006", api_key=None):
        self.host = host
        self.auth_header = {'Authorization': 'Bearer %s' % api_key}

    def state_county_data(self, listings, span, attribute):
        return json.loads(requests.get(urlparse.urljoin(self.host, "heatmap/onbroad/?format=json&listingtype=%s&span=%s&attribute=%s" % (listings, span, attribute)), headers=self.auth_header).text)

    def zip_data(self, listings, radius, latitude, longitude, span, attribute):
        return json.loads(requests.get(urlparse.urljoin(self.host, "heatmap/onzip/?format=json&listingtype=%s&radius=%s&latitude=%s&longitude=%s&span=%s&attribute=%s" % (listings, radius, latitude, longitude, span, attribute)), headers=self.auth_header).text)
