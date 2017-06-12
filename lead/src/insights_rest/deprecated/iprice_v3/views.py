'''
Created on 02-Jun-2016

@author: root

'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from pymongo import MongoClient
from pyzipcode import Pyzipcode as pz


@permission_classes((permissions.AllowAny,))
class iPriceTrendViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        iPrice Trend Version 3.0 with  new property types

       1.'TownHouse',
       2.'Multifamily'
       3.'All'

        and Date format (timestamp) in milliseconds.

        url:https://insights.propmix.io:8004/iprice/v3/trend

        ---
        # YAML (must be separated by `---`)
        type:
          schema : {zip_code_location: string, last_3_year_avg_l_s_ratio: string, last_3_months_trend_variation: string, last_3_months_price_trend_percentage: string, last_3_months_price_trend_change: string, last_3_month_data: string, l_s_ratio_recent: string}
          zip_code_location:
            required: true
            type: set
            sample:
                nested:
                    required: true
                    type: object

          last_3_year_avg_l_s_ratio:
            required: false
            type: string
          last_3_months_trend_variation:
            required: false
            type: string

        omit_serializer: false

        parameters_strategy: merge
        omit_parameters:
            - path
        parameters:
            - name: zip
              description: Postalcode which iPriceTrend to be calculated.
              type: string
              paramType: query
              defaultValue: 33134
            - name: type
              description: Property types (or building types) fields to describe the kind of property for sale in Postal code.
              paramType: query

        responseMessages:
            - code: 401
              message: Not authenticated
            - code : 404
              message: Not Found
            - code : ERROR
              message : No Zip Specified or Invalid Zip

        consumes:
            - application/json
            - application/xml
        produces:
            - application/json
            - application/xml
        """
        try:
            if not request.query_params['zip'].isdigit():
                return Response({'status': 'ERROR', 'error': 'INVALID_ZIP'})
            if ('type' in request.query_params):
                p_type = request.query_params['type']
            else:
                p_type = 'SingleFamily'
        except:
            return Response({'status': 'ERROR', 'error': 'NO_ZIP_SPECIFIED'})
        db_client = MongoClient('mongo-master.propmix.io', 33017)

        try:
            zipcode = pz.get(str(request.query_params['zip']), "US")
        except:
            return Response({'status': 'ERROR', 'error': 'Invalid ZipCode'})
        zip_code_location = ', '.join([zipcode['county'], zipcode['state_short']])

        data = list(db_client.iestimate.rets_standardized_data_nxmodel_01.find({"postalcode": str(request.query_params['zip'])}))
        if len(data) == 0:
            return Response({'status': 'ERROR', 'error': 'Insufficient data'})
        else:
            last_3_month_meta = data[0]['3_month_meta'][p_type]['price_trend'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None
            last_6_month_meta = data[0]['6_month_meta'][p_type]['price_trend'] if data[0]['6_month_meta'][p_type] is not None and data[0]['6_month_meta'][p_type]['price_trend'] != {} else None
            last_12_month_meta = data[0]['12_month_meta'][p_type]['price_trend'] if data[0]['12_month_meta'][p_type] is not None and data[0]['12_month_meta'][p_type]['price_trend'] != {} else None
            last_36_month_meta = data[0]['36_month_meta'][p_type]['price_trend'] if data[0]['36_month_meta'][p_type] is not None and data[0]['36_month_meta'][p_type]['price_trend'] != {} else None
            last_60_month_meta = data[0]['60_month_meta'][p_type]['price_trend'] if data[0]['60_month_meta'][p_type] is not None and data[0]['60_month_meta'][p_type]['price_trend'] != {} else None
            l_s_ratio_recent = data[0]['3_month_meta'][p_type]['price_trend']['lsratio'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None

            last_3_month_avg_l_s_ratio = data[0]['3_month_meta'][p_type]['price_trend']['avglsratio'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None
            last_6_month_avg_l_s_ratio = data[0]['6_month_meta'][p_type]['price_trend']['avglsratio'] if data[0]['6_month_meta'][p_type] is not None and data[0]['6_month_meta'][p_type]['price_trend'] != {} else None
            last_1_year_avg_l_s_ratio = data[0]['12_month_meta'][p_type]['price_trend']['avglsratio'] if data[0]['12_month_meta'][p_type] is not None and data[0]['12_month_meta'][p_type]['price_trend'] != {} else None
            last_3_year_avg_l_s_ratio = data[0]['36_month_meta'][p_type]['price_trend']['avglsratio'] if data[0]['36_month_meta'][p_type] is not None and data[0]['36_month_meta'][p_type]['price_trend'] != {} else None
            last_5_year_avg_l_s_ratio = data[0]['60_month_meta'][p_type]['price_trend']['avglsratio'] if data[0]['60_month_meta'][p_type] is not None and data[0]['60_month_meta'][p_type]['price_trend'] != {} else None

            curr_open_listings = data[0]['3_month_meta'][p_type]['price_trend']['openlistings'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None
            curr_pending_sale = data[0]['3_month_meta'][p_type]['price_trend']['pendingsale'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None

            last_3_month_total_txn = data[0]['3_month_meta'][p_type]['price_trend']['totaltxn'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None
            last_6_month_total_txn = data[0]['6_month_meta'][p_type]['price_trend']['totaltxn'] if data[0]['6_month_meta'][p_type] is not None and data[0]['6_month_meta'][p_type]['price_trend'] != {} else None
            last_1_year_total_txn = data[0]['12_month_meta'][p_type]['price_trend']['totaltxn'] if data[0]['12_month_meta'][p_type] is not None and data[0]['12_month_meta'][p_type]['price_trend'] != {} else None
            last_3_year_total_txn = data[0]['36_month_meta'][p_type]['price_trend']['totaltxn'] if data[0]['36_month_meta'][p_type] is not None and data[0]['36_month_meta'][p_type]['price_trend'] != {} else None
            last_5_year_total_txn = data[0]['60_month_meta'][p_type]['price_trend']['totaltxn'] if data[0]['60_month_meta'][p_type] is not None and data[0]['60_month_meta'][p_type]['price_trend'] != {} else None

            last_3_month_avg_txn_per_week = data[0]['3_month_meta'][p_type]['price_trend']['avgtxn'] if data[0]['3_month_meta'][p_type] is not None and data[0]['3_month_meta'][p_type]['price_trend'] != {} else None
            last_6_month_avg_txn_per_week = data[0]['6_month_meta'][p_type]['price_trend']['avgtxn'] if data[0]['6_month_meta'][p_type] is not None and data[0]['6_month_meta'][p_type]['price_trend'] != {} else None
            last_1_year_avg_txn_per_week = data[0]['12_month_meta'][p_type]['price_trend']['avgtxn'] if data[0]['12_month_meta'][p_type] is not None and data[0]['12_month_meta'][p_type]['price_trend'] != {} else None
            last_3_year_avg_txn_per_week = data[0]['36_month_meta'][p_type]['price_trend']['avgtxn'] if data[0]['36_month_meta'][p_type] is not None and data[0]['36_month_meta'][p_type]['price_trend'] != {} else None
            last_5_year_avg_txn_per_week = data[0]['60_month_meta'][p_type]['price_trend']['avgtxn'] if data[0]['60_month_meta'][p_type] is not None and data[0]['60_month_meta'][p_type]['price_trend'] != {} else None

            week_52_high = data[0]['12_month_meta'][p_type]['price_trend']['week_52_high'] if data[0]['12_month_meta'][p_type] is not None and data[0]['12_month_meta'][p_type]['price_trend'] != {} else None
            week_52_low = data[0]['12_month_meta'][p_type]['price_trend']['week_52_low'] if data[0]['12_month_meta'][p_type] is not None and data[0]['12_month_meta'][p_type]['price_trend'] != {} else None

            import datetime
            epoch = datetime.datetime.utcfromtimestamp(0)

            def unix_time_millis(dt):
                return (dt - epoch).total_seconds() * 1000.0
            if last_3_month_meta is not None:
                last_3_month_meta["series"] = [{key: sorted(map(lambda k: [unix_time_millis(datetime.datetime.strptime(k[0], '%d/%m/%Y')), k[1]], item[key]), key=lambda k: k[0])} for item in last_3_month_meta["series"] for key in item.keys()]
            if last_6_month_meta is not None:
                last_6_month_meta["series"] = [{key: sorted(map(lambda k: [unix_time_millis(datetime.datetime.strptime(k[0], '%d/%m/%Y')), k[1]], item[key]), key=lambda k: k[0])} for item in last_6_month_meta["series"] for key in item.keys()] if last_6_month_meta is not None else None
            if last_12_month_meta is not None:
                last_12_month_meta["series"] = [{key: sorted(map(lambda k: [unix_time_millis(datetime.datetime.strptime(k[0], '%d/%m/%Y')), k[1]], item[key]), key=lambda k: k[0])} for item in last_12_month_meta["series"] for key in item.keys()] if last_12_month_meta is not None else None
            if last_36_month_meta is not None:
                last_36_month_meta["series"] = [{key: sorted(map(lambda k: [unix_time_millis(datetime.datetime.strptime(k[0], '%d/%m/%Y')), k[1]], item[key]), key=lambda k: k[0])} for item in last_36_month_meta["series"] for key in item.keys()] if last_36_month_meta is not None else None
            if last_60_month_meta is not None:
                last_60_month_meta["series"] = [{key: sorted(map(lambda k: [unix_time_millis(datetime.datetime.strptime(k[0], '%d/%m/%Y')), k[1]], item[key]), key=lambda k: k[0])} for item in last_60_month_meta["series"] for key in item.keys()] if last_60_month_meta is not None else None

            return Response({"zip_code_location": zip_code_location,
                             "last_3_months_price_per_square_feet": last_3_month_meta["series"][0]['price_per_square_feet'][-1][1] if last_3_month_meta is not None else None,
                             "last_3_months_trend_variation": abs(last_3_month_meta["series"][0]['price_per_square_feet'][0][1] - last_3_month_meta["series"][0]['price_per_square_feet'][-1][1]) if last_3_month_meta is not None else None,
                             "last_3_months_price_trend_percentage": float(abs(last_3_month_meta["series"][0]['price_per_square_feet'][0][1] - last_3_month_meta["series"][0]['price_per_square_feet'][-1][1])) / float(last_3_month_meta["series"][0]['price_per_square_feet'][0][1]) if last_3_month_meta is not None else None,
                             "last_3_months_price_trend_change": ("+" if last_3_month_meta["series"][0]['price_per_square_feet'][-1][1] - last_3_month_meta["series"][0]['price_per_square_feet'][0][1] >= 0 else "-") if last_3_month_meta is not None else None,
                             "last_3_month_data": last_3_month_meta["series"] if last_3_month_meta is not None else None,
                             "last_6_month_data": last_6_month_meta["series"] if last_6_month_meta is not None else None,
                             "last_1_year_data": last_12_month_meta["series"] if last_12_month_meta is not None else None,
                             "last_3_year_data": last_36_month_meta["series"] if last_36_month_meta is not None else None,
                             "last_5_year_data": last_60_month_meta["series"] if last_60_month_meta is not None else None,
                             "start_to_end_data": last_60_month_meta["series"] if last_60_month_meta is not None else None,
                             "l_s_ratio_recent": l_s_ratio_recent,
                             "last_3_month_avg_l_s_ratio": last_3_month_avg_l_s_ratio,
                             "last_6_month_avg_l_s_ratio": last_6_month_avg_l_s_ratio,
                             "last_1_year_avg_l_s_ratio": last_1_year_avg_l_s_ratio,
                             "last_3_year_avg_l_s_ratio": last_3_year_avg_l_s_ratio,
                             "last_5_year_avg_l_s_ratio": last_5_year_avg_l_s_ratio,
                             "curr_open_listings": curr_open_listings,
                             "curr_pending_sale": curr_pending_sale,
                             "last_3_month_total_txn": last_3_month_total_txn,
                             "last_6_month_total_txn": last_6_month_total_txn,
                             "last_1_year_total_txn": last_1_year_total_txn,
                             "last_3_year_total_txn": last_3_year_total_txn,
                             "last_5_year_total_txn": last_5_year_total_txn,

                             "last_3_month_avg_txn_per_week": last_3_month_avg_txn_per_week,
                             "last_6_month_avg_txn_per_week": last_6_month_avg_txn_per_week,
                             "last_1_year_avg_txn_per_week": last_1_year_avg_txn_per_week,
                             "last_3_year_avg_txn_per_week": last_3_year_avg_txn_per_week,
                             "last_5_year_avg_txn_per_week": last_5_year_avg_txn_per_week,
                             "week_52_low": week_52_low,
                             "week_52_high": week_52_high,
                             "start_to_end_total_txs": last_5_year_total_txn,
                             "start_to_end_avg_txs_per_week": last_5_year_avg_txn_per_week,
                             "start_to_end_avg_l_s_ratio": last_5_year_avg_l_s_ratio,
                             })


@permission_classes((permissions.AllowAny,))
class iZipStatusViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        iPrice Trend Version 3.0 zipStatus
        It will returns the property types status of all availabiltiy postalcodes.

        """
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        zip_status = db_client.iestimate.rets_standardized_data_zipstatus.find_one({"version": "v3"})['ministatus']
        return Response(zip_status)
