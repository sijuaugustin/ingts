'''
Created on Dec 29, 2016

@author: joseph
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
import pymongo
from pymongo import MongoClient
from .dbauth import DATABASE_ACCESS
from cognub.propmixapi.pricetrendapi import PriceTrendAPI
from datetime import datetime
import statistics
from __builtin__ import reduce


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def datetime_from_millis(millis):
    return datetime.fromtimestamp(millis/1000.0)


@permission_classes((permissions.AllowAny,))
class HPIRawViewset(viewsets.ViewSet):

    def list(self, request):
        """
            HPIRawData

            API will return HPI raw data

            ---

            type:
              schema : {period: int, yr: int, index_nsa: float }
            parameters_strategy: merge
            omit_parameters:
                - path
            parameters:
                - name: span
                  description: start year - end year
                  required: true
                  type: string
                  paramType: query
                  defaultValue: 2000-2016
                - name: location
                  description: location name should be one from HPIRawLocations API
                  required: true
                  paramType: query
                  defaultValue: East North Central Division
                - name: frequency
                  description: monthly/quarterly
                  required: true
                  paramType: query
                  defaultValue: monthly

            consumes:
                - application/json
            produces:
                - application/json
        """
        span = map(int, request.query_params['span'].split('-'))
        location = request.query_params['location']
        frequency = request.query_params['frequency']
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        records = list(db_client.ipricetrend.hpiraw.find(
            {'yr': {'$lte': span[1], '$gte': span[0]},
             'place_name': location, 'frequency': frequency,
             'hpi_flavor': "all-transactions" if frequency == "quarterly"
             else {"$ne": None}},
            {'_id': False, 'index_sa': True, 'index_nsa': True,
             'yr': True, 'period': True}).sort([("yr", pymongo.ASCENDING),
                                                ("period", pymongo.ASCENDING)]
                                               ))
        return Response(records)


@permission_classes((permissions.AllowAny,))
class HPIPlaceNames(viewsets.ViewSet):

    def list(self, request):
        """
            HPILocations

            API will return the HPI available locations
        """
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        locationrecords = list(db_client.ipricetrend.hpiraw.distinct("place_name"))
        return Response(locationrecords)


@permission_classes((permissions.AllowAny,))
class HPIYears(viewsets.ViewSet):

    def list(self, request):
        """
            HPIYears

            API will return the HPI available years
        """
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        yr = list(db_client.ipricetrend.hpiraw.distinct("yr"))
        return Response(yr)


@permission_classes((permissions.AllowAny,))
class HPI3ZipRawData(viewsets.ViewSet):

    def list(self, request):
        """
            HPI3ZipRawData

            API will return HPI 3Zip Raw Data

            ---

            type:
              schema : {Quarter: int, Year: int, Index (NSA): float }
            parameters_strategy: merge
            omit_parameters:
                - path
            parameters:
                - name: span
                  description: start year - end year
                  required: true
                  type: string
                  paramType: query
                  defaultValue: 2000-2016
                - name: zip
                  description: 3zip name should be one from HPI3Zips API or equilant 5digit
                  required: true
                  type: string
                  paramType: query
                  defaultValue: '23010'

            consumes:
                - application/json
            produces:
                - application/json
        """
        span = map(int, request.query_params['span'].split('-'))
        three_digit_zip = int(request.query_params['zip'][:3])
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        records = list(db_client.ipricetrend.hpi3digitzip.find(
            {'Year': {'$lte': span[1], '$gte': span[0]},
             'Three-Digit ZIP Code': three_digit_zip,
             'Index Type': {"$ne": None}},
            {'_id': False, 'Index (NSA)': True,
             'Year': True, 'Quarter': True}).sort([("Year", pymongo.ASCENDING),
                                                   ("Quarter", pymongo.ASCENDING)]
                                                  ))
        return Response(records)


@permission_classes((permissions.AllowAny,))
class HPI3Zips(viewsets.ViewSet):

    def list(self, request):
        """
            HPI3Zips

            API will return the HPI available 3Zips
        """
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        locationrecords = list(db_client.ipricetrend.hpi3digitzip.distinct("Three-Digit ZIP Code"))
        return Response(locationrecords)


@permission_classes((permissions.AllowAny,))
class HPI3ZipYears(viewsets.ViewSet):

    def list(self, request):
        """
            HPI3ZipYears

            API will return the HPI3Zip available years
        """
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        yr = list(db_client.ipricetrend.hpi3digitzip.distinct("Year"))
        return Response(yr)


@permission_classes((permissions.AllowAny,))
class HPIPriceTrendMix(viewsets.ViewSet):

    def ipt_to_quarter(self, ipt_w):
        ipt_q = []
        q_cache = []
        for index, val in enumerate(ipt_w):
            val_date = datetime_from_millis(val[0])
            val_ppsqft = val[1]
            q_record = {'yr': val_date.year, 'quarter': (val_date.month/4) + 1, 'ppsqft': val_ppsqft}
            if index == 0 or (q_cache[-1]['yr'] == q_record['yr'] and q_cache[-1]['quarter'] == q_record['quarter']):
                q_cache.append(q_record)
            else:
                q_med = statistics.median(map(lambda x: x['ppsqft'], q_cache))
                q_avg = reduce(lambda x, y: {'ppsqft': x['ppsqft'] + y['ppsqft']}, q_cache)['ppsqft']/float(len(q_cache))
                ipt_q.append({'yr': q_cache[-1]['yr'], 'quarter': q_cache[-1]['quarter'], 'ppsqft_avg': q_avg, 'ppsqft_med': q_med})
                del q_cache[:]
                q_cache.append(q_record)
        return ipt_q

    def list(self, request):
        """
            HPIPriceTrendMix

            API will return HPI 3Zip + PriceTrend

            ---

            type:
              schema : {Quarter: int, Year: int, Index (NSA): float }
            parameters_strategy: merge
            omit_parameters:
                - path
            parameters:
                - name: span
                  description: start year - end year
                  required: true
                  type: string
                  paramType: query
                  defaultValue: 2000-2016
                - name: zip
                  description: 3zip name should be one from HPI3Zips API or equilant 5digit
                  required: true
                  type: string
                  paramType: query
                  defaultValue: '23010'

            consumes:
                - application/json
            produces:
                - application/json
        """
        span = map(int, request.query_params['span'].split('-'))
        three_digit_zip_str = request.query_params['zip'][:3]
        three_digit_zip = int(three_digit_zip_str)
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.ipricetrend.authenticate(**DATABASE_ACCESS)
        records = list(db_client.ipricetrend.hpi3digitzip.find(
            {'Year': {'$lte': span[1], '$gte': span[0]},
             'Three-Digit ZIP Code': three_digit_zip,
             'Index Type': {"$ne": None}},
            {'_id': False, 'Index (NSA)': True,
             'Year': True, 'Quarter': True}).sort([("Year", pymongo.ASCENDING),
                                                   ("Quarter", pymongo.ASCENDING)]
                                                  ))
        ptapi = PriceTrendAPI(api_key="ncY3iV454RWqflNROGfhcC0NrGTwOF")
        price_trends = []
        zip_status = ptapi.get_zipstatus()
        zip_list = map(lambda x: x['postalcode'], zip_status)
        for postal in [postal for postal in zip_list if postal.startswith(three_digit_zip_str)][:10]:
            trend = ptapi.get_trend(postal)
            if 'last_3_year_data' in trend and trend['last_3_year_data'] is not None:
                price_trends.append({'zip': postal, '3y_trend': self.ipt_to_quarter(trend['last_3_year_data'][0]['price_per_square_feet'])})
        return Response({'hpi': records, 'price_trends': price_trends})

if __name__ == '__main__':
    now = datetime.now()
    millis = unix_time_millis(now)
    print datetime_from_millis(millis)