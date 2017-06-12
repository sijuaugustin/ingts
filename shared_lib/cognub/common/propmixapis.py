'''
Created on Dec 9, 2016

@author: joseph
'''
import requests
import urllib2
import json
import warnings
import time


class PropMixAPISet():

    @staticmethod
    def radius_search(params,
                      radius_host='https://dev-api.propmix.io/mlslite/icma/v1/GetListingsByRadius',
                      is_zip_on=1):
        warnings.warn("deprecated please use radius_api instead",
                      DeprecationWarning)
        url_pattern = "%s?Street={address}&Radius={radius}&MonthsBack={months_back}&City={city}&State={state}&PropertyType={property_type}&PageSize={page_size}&Longitude={longitude}&Latitude={latitude}&Zip={zip}&isZipON=%d" %\
            (radius_host, is_zip_on)
        url_pattern = url_pattern.format(**params)
        response = requests.get(url_pattern).text
        print response
        return json.loads(response)

    @staticmethod
    def radius_search_api(params,
                      radius_host='https://api.propmix.io/mlslite/icma/v1/GetListingsByRadius',
                      is_zip_on=1):
        warnings.warn("deprecated please use radius_api instead",
                      DeprecationWarning)
        url_pattern = "%s?Street={address}&Radius={radius}&MonthsBack={months_back}&City={city}&State={state}&PropertyType={property_type}&PageSize={page_size}&Longitude={longitude}&Latitude={latitude}&Zip={zip}&isZipON=%d" %\
            (radius_host, is_zip_on)
        url_pattern = url_pattern.format(**params)
        response = requests.get(url_pattern).text
        return json.loads(response)

    @staticmethod
    def radius_search_api_v2(params,
                      radius_host= 'https://api.propmix.io/mlslite/val/v1/GetListingsByRadius',
                      is_zip_on=1):
        warnings.warn("deprecated please use radius_api instead",
                      DeprecationWarning)
        url_pattern = "%s?Street={address}&access_token={access_token}&OrderId={OrderId}&EffectiveDate={EffectiveDate}&PropertyType={PropertyType}&MlsStatus={MlsStatus}&PropertySubType={Property_SubType}&MinBed={MinBed}&MaxBed={MaxBed}&MinBath={MinBath}&MaxBath={MaxBath}&Radius={radius}&MonthsBack={months_back}&City={city}&State={state}&PageSize={page_size}&Zip={zip}&isZipON=%d&imagesON={imagesON}&Rental={Rental}" %\
            (radius_host ,is_zip_on)
        url_pattern = url_pattern.format(**params)
        response = requests.get(url_pattern).text
        return json.loads(response)

    @staticmethod
    def radius_api(params, radius_host='https://dev-api.propmix.io/mlslite/\
    icma/v1/GetListingsByRadius', is_zip_on=1):
        url_pattern = '%s?' + \
            '&'.join(map(lambda x: '%s=%s' % (x[0], str(x[1])),
                         params.items()))
        response = requests.get(url_pattern).text
        return json.loads(response)

if __name__ == '__main__':
    params = {"address": urllib2.quote(
        '211 Fuller Rd, HINSDALE, IL 60521, USA'),
              "radius": 90.0,
              "state": 'IL',
              "months_back": 36,
              "city": 'Hinsdale',
              "page_size": 80,
              "property_type": 'Residential',
              "latitude": 41.2171767186,
              "longitude": -73.0760858249,
              "zip": '06461'
              }
    print PropMixAPISet.radius_search(params)
