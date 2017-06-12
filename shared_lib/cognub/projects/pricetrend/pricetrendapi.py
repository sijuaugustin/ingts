'''
Created on Oct 26, 2016

@author: joseph
'''
import urlparse
import json
import requests
import numpy as np
from sklearn.linear_model import LinearRegression


class InvalidSpanError(Exception):
    pass


def unix_time_millis(dt):
    import datetime
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


class PriceTrendAPI():
    span_map = {'3M': '3_month',
                '6M': '6_month',
                '1Y': '1_year',
                '3Y': '3_year',
                '5Y': '5_year'}

    def __init__(self, host="https://insights.propmix.io:8006", api_key='7yah6X850YDrpT8xdtEIJZOA6oAujz'):
        self.host = host
        self.api_key = api_key

    def get_trend(self, postalcode, property_type="All"):
        return json.loads(requests.get(urlparse.urljoin(self.host, "iprice/mlslite/trend/?format=json&zip=%s&type=%s" % (postalcode, property_type)), headers={"Authorization": "Bearer %s" % (self.api_key)}).text)

    def get_zipstatus(self):
        return json.loads(requests.get(urlparse.urljoin(self.host, "iprice/mlslite/zipstatus"), headers={"Authorization": "Bearer %s" % (self.api_key)}).text)

    def get_regression_model(self, trend, span="3M"):
        if span not in self.span_map:
            raise InvalidSpanError()
        lr_model = LinearRegression()
        ppsf_trend = trend["last_%s_data" % (self.span_map[span])][0]["price_per_square_feet"]
        print np.asarray(map(lambda x: [x[0]], ppsf_trend)).shape
        lr_model.fit(np.asarray(map(lambda x: [x[0]], ppsf_trend)), np.asarray(map(lambda x: [x[1]], ppsf_trend)))
        return lr_model

    def get_future_trend(self, trend, date_list, span="3M"):
        lr_model = self.get_regression_model(trend, span)
        return lr_model.predict(np.asarray(map(lambda x: [unix_time_millis(x)], date_list)))

if __name__ == "__main__":
    import datetime
    #from cognub.projects.pricetrend.pricetrendapi import PriceTrendAPI
    print PriceTrendAPI().get_zipstatus()
    iprice = PriceTrendAPI()
    trend = iprice.get_trend("33156")
    print iprice.get_future_trend(trend, date_list=np.asarray([datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=7)]), span="6M")
