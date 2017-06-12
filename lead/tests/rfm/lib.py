'''
Created on Dec 15, 2016

@author: vishnu.sk
'''
import urlparse
import json
import requests


class RFMapi():
    def __init__(self, host="https://insights.propmix.io:8006", api_key=None):
        self.host = host
        self.auth_header = {'Authorization': 'Bearer %s' % api_key}

    def best_fit(self, address, SI_PropertyType, Zip, radius, GLA, Beds, Baths, LotSizeArea, YearBuilt, StoriesTotal, Distance, MonthsBack, City, State):
        return json.loads(requests.get(urlparse.urljoin(self.host, "rfm/agents/bestfit/?format=json&address=%s&SI_PropertyType=%s&Zip=%s&radius=%s&GLA=%s&Beds=%s&Baths=%s&LotSizeArea=%s&YearBuilt=%s&StoriesTotal=%s&Distance=%s&MonthsBack=%s&City=%s&State=%s" % (address, SI_PropertyType, Zip, radius, GLA, Beds, Baths, LotSizeArea, YearBuilt, StoriesTotal, Distance, MonthsBack, City, State)), headers=self.auth_header).text)

    def get_details(self, agent, State, zip):
        return json.loads(requests.get(urlparse.urljoin(self.host, "rfm/agent/details/?format=json&agent=%s&State=%s&zip=%s" % (agent, State, zip)), headers=self.auth_header).text)

    def get_top10(self, level, value):
        return json.loads(requests.get(urlparse.urljoin(self.host, "rfm/agents/topten/?format=json&level=%s&value=%s" % (level, value)), headers=self.auth_header).text)
