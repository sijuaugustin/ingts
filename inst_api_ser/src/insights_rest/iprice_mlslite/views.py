from rest_framework import viewsets
from rest_framework.response import Response
from pymongo import MongoClient
from pyzipcode import Pyzipcode as pz
from rest_framework_tracking.mixins import LoggingMixin
from oauth2_provider.ext.rest_framework import OAuth2Authentication,\
    TokenHasScope
from .dbauth import DATABASE_ACCESS


class iPriceTrendViewSet(LoggingMixin, viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def list(self, request):
        """
        iPrice Trend MLSLite

        Will respond back with Price Trend on particular postalcode for different property types.

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
              description: Property types (should be one of 'TownHouse', 'Multifamily', 'Single Family', 'All')
              paramType: query
        responseMessages:
            - code: 401
              message: Not Authorized
            - code : 404
              message: Not Found

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

        try:
            zipcode = pz.get(str(request.query_params['zip']), "US")
            if not zipcode:
                return Response({'status': 'ERROR',
                                 'error': 'Invalid ZipCode'})
        except:
            return Response({'status': 'ERROR', 'error': 'Invalid ZipCode'})
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.infodb.authenticate(**DATABASE_ACCESS)
        zip_status_list =\
            db_client['infodb']['mlslite_unique_data_zipstatus.s']\
            .find_one({"version": "v3"})['ministatus']
        for status in zip_status_list:
            if status['postalcode'] == str(request.query_params['zip']):
                break
        else:
            return Response({'status':'ERROR',
                             'error':'NO DATA FOR POSTALCODE'})
        zip_code_location = ', '.join([zipcode['county'],
                                       zipcode['state_short']])
        db_client.mlmodeldb.authenticate(**DATABASE_ACCESS)
        data = list(db_client['mlmodeldb']['mlslite_unique_data_nxmodel.s']
                    .find({"postalcode": str(request.query_params['zip'])}))
        db_client.close()
        if len(data) == 0:
            return Response({'status': 'ERROR', 'error': 'Insufficient data'})
        else:
            last_3_month_meta =\
                data[0]['3_month_meta'][p_type]['price_trend']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_6_month_meta =\
                data[0]['6_month_meta'][p_type]['price_trend']\
                if '6_month_meta' in data[0]\
                and data[0]['6_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['6_month_meta'][p_type]\
                and data[0]['6_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_12_month_meta =\
                data[0]['12_month_meta'][p_type]['price_trend']\
                if '12_month_meta' in data[0]\
                and data[0]['12_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['12_month_meta'][p_type]\
                and data[0]['12_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_36_month_meta =\
                data[0]['36_month_meta'][p_type]['price_trend']\
                if '36_month_meta'in data[0]\
                and data[0]['36_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['36_month_meta'][p_type]\
                and data[0]['36_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_60_month_meta =\
                data[0]['60_month_meta'][p_type]['price_trend']\
                if '60_month_meta' in data[0]\
                and data[0]['60_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['60_month_meta'][p_type]\
                and data[0]['60_month_meta'][p_type]['price_trend'] != {}\
                else None
            l_s_ratio_recent =\
                data[0]['3_month_meta'][p_type]['price_trend']['lsratio']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_3_month_avg_l_s_ratio =\
                data[0]['3_month_meta'][p_type]['price_trend']['avglsratio']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_6_month_avg_l_s_ratio =\
                data[0]['6_month_meta'][p_type]['price_trend']['avglsratio']\
                if '6_month_meta' in data[0]\
                and data[0]['6_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['6_month_meta'][p_type]\
                and data[0]['6_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_1_year_avg_l_s_ratio =\
                data[0]['12_month_meta'][p_type]['price_trend']['avglsratio']\
                if '12_month_meta' in data[0]\
                and data[0]['12_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['12_month_meta'][p_type]\
                and data[0]['12_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_3_year_avg_l_s_ratio =\
                data[0]['36_month_meta'][p_type]['price_trend']['avglsratio']\
                if '36_month_meta'in data[0]\
                and data[0]['36_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['36_month_meta'][p_type]\
                and data[0]['36_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_5_year_avg_l_s_ratio =\
                data[0]['60_month_meta'][p_type]['price_trend']['avglsratio']\
                if '60_month_meta' in data[0]\
                and data[0]['60_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['60_month_meta'][p_type]\
                and data[0]['60_month_meta'][p_type]['price_trend'] != {}\
                else None
            curr_open_listings =\
                data[0]['3_month_meta'][p_type]['price_trend']['openlistings']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            curr_pending_sale =\
                data[0]['3_month_meta'][p_type]['price_trend']['pendingsale']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_3_month_total_txn =\
                data[0]['3_month_meta'][p_type]['price_trend']['totaltxn']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_6_month_total_txn =\
                data[0]['6_month_meta'][p_type]['price_trend']['totaltxn']\
                if '6_month_meta' in data[0]\
                and data[0]['6_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['6_month_meta'][p_type]\
                and data[0]['6_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_1_year_total_txn =\
                data[0]['12_month_meta'][p_type]['price_trend']['totaltxn']\
                if '12_month_meta' in data[0]\
                and data[0]['12_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['12_month_meta'][p_type]\
                and data[0]['12_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_3_year_total_txn =\
                data[0]['36_month_meta'][p_type]['price_trend']['totaltxn']\
                if '36_month_meta'in data[0]\
                and data[0]['36_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['36_month_meta'][p_type]\
                and data[0]['36_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_5_year_total_txn =\
                data[0]['60_month_meta'][p_type]['price_trend']['totaltxn']\
                if '60_month_meta' in data[0]\
                and data[0]['60_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['60_month_meta'][p_type]\
                and data[0]['60_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_3_month_avg_txn_per_week =\
                data[0]['3_month_meta'][p_type]['price_trend']['avgtxn']\
                if '3_month_meta' in data[0]\
                and data[0]['3_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['3_month_meta'][p_type]\
                and data[0]['3_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_6_month_avg_txn_per_week =\
                data[0]['6_month_meta'][p_type]['price_trend']['avgtxn']\
                if '6_month_meta' in data[0]\
                and data[0]['6_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['6_month_meta'][p_type]\
                and data[0]['6_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_1_year_avg_txn_per_week =\
                data[0]['12_month_meta'][p_type]['price_trend']['avgtxn']\
                if '12_month_meta' in data[0]\
                and data[0]['12_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['12_month_meta'][p_type]\
                and data[0]['12_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_3_year_avg_txn_per_week =\
                data[0]['36_month_meta'][p_type]['price_trend']['avgtxn']\
                if '36_month_meta'in data[0]\
                and data[0]['36_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['36_month_meta'][p_type]\
                and data[0]['36_month_meta'][p_type]['price_trend'] != {}\
                else None
            last_5_year_avg_txn_per_week =\
                data[0]['60_month_meta'][p_type]['price_trend']['avgtxn']\
                if '60_month_meta' in data[0]\
                and data[0]['60_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['60_month_meta'][p_type]\
                and data[0]['60_month_meta'][p_type]['price_trend'] != {}\
                else None
            week_52_high =\
                data[0]['12_month_meta'][p_type]['price_trend']['week_52_high']\
                if '12_month_meta' in data[0]\
                and data[0]['12_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['12_month_meta'][p_type]\
                and data[0]['12_month_meta'][p_type]['price_trend'] != {}\
                else None
            week_52_low =\
                data[0]['12_month_meta'][p_type]['price_trend']['week_52_low']\
                if '12_month_meta' in data[0]\
                and data[0]['12_month_meta'][p_type] is not None\
                and 'price_trend' in data[0]['12_month_meta'][p_type]\
                and data[0]['12_month_meta'][p_type]['price_trend'] != {}\
                else None
            import datetime
            epoch = datetime.datetime.utcfromtimestamp(0)

            def unix_time_millis(dt):
                return (dt - epoch).total_seconds() * 1000.0
            if last_3_month_meta is not None:
                last_3_month_meta["series"] =\
                    [{key: sorted(
                        map(lambda k: [
                            unix_time_millis(
                                datetime.datetime
                                .strptime(k[0], '%d/%m/%Y')),
                            k[1]], item[key]), key=lambda k: k[0])}
                     for item in last_3_month_meta["series"]
                     for key in item.keys()]
            if last_6_month_meta is not None:
                last_6_month_meta["series"] =\
                    [{key: sorted(
                        map(lambda k: [
                            unix_time_millis(
                                datetime.datetime.strptime(k[0], '%d/%m/%Y')),
                            k[1]], item[key]), key=lambda k: k[0])}
                     for item in last_6_month_meta["series"]
                     for key in item.keys()]\
                    if last_6_month_meta is not None else None
            if last_12_month_meta is not None:
                last_12_month_meta["series"] =\
                    [{key: sorted(map(lambda k:
                                      [unix_time_millis(
                                          datetime.datetime
                                          .strptime(k[0], '%d/%m/%Y')),
                                       k[1]], item[key]), key=lambda k: k[0])}
                     for item in last_12_month_meta["series"]
                     for key in item.keys()]\
                    if last_12_month_meta is not None else None
            if last_36_month_meta is not None:
                last_36_month_meta["series"] =\
                    [{key: sorted(map(lambda k:
                                  [unix_time_millis(
                                      datetime.datetime
                                      .strptime(k[0], '%d/%m/%Y')), k[1]],
                                      item[key]), key=lambda k: k[0])}
                     for item in last_36_month_meta["series"]
                     for key in item.keys()]\
                    if last_36_month_meta is not None else None
            if last_60_month_meta is not None:
                last_60_month_meta["series"] =\
                    [{key: sorted(map(lambda k:
                                      [unix_time_millis(
                                          datetime.datetime
                                          .strptime(k[0], '%d/%m/%Y')), k[1]],
                                      item[key]), key=lambda k: k[0])}
                     for item in last_60_month_meta["series"]
                     for key in item.keys()]\
                    if last_60_month_meta is not None else None

            return Response({
                            "zip_code_location": zip_code_location,
                            #                          "property_type":type,
                            "last_3_months_price_per_square_feet":
                            last_3_month_meta["series"][0]
                            ['price_per_square_feet'][-1][1]\
                            if last_3_month_meta is not None else None,
                            "last_3_months_trend_variation":
                            abs(last_3_month_meta["series"][0]
                                ['price_per_square_feet'][0][1]\
                                - last_3_month_meta["series"][0]
                                ['price_per_square_feet'][-1][1])\
                                if last_3_month_meta is not None else None,
                            "last_3_months_price_trend_percentage":
                            float(abs(last_3_month_meta["series"][0]
                                      ['price_per_square_feet'][0][1]\
                                      - last_3_month_meta["series"][0]
                                      ['price_per_square_feet'][-1][1]))\
                            / float(last_3_month_meta["series"][0]
                                    ['price_per_square_feet'][0][1])\
                                if last_3_month_meta is not None else None,
                            "last_3_months_price_trend_change":
                            ("+" if last_3_month_meta["series"][0]
                             ['price_per_square_feet'][-1][1]\
                             - last_3_month_meta["series"][0]
                             ['price_per_square_feet'][0][1] >= 0 else "-")\
                                if last_3_month_meta is not None else None,
                            "last_3_month_data":
                            last_3_month_meta["series"]\
                            if last_3_month_meta is not None else None,
                            "last_6_month_data":
                            last_6_month_meta["series"]\
                            if last_6_month_meta is not None else None,
                            "last_1_year_data":
                            last_12_month_meta["series"]\
                            if last_12_month_meta is not None else None,
                            "last_3_year_data":
                            last_36_month_meta["series"]\
                            if last_36_month_meta is not None else None,
                            "last_5_year_data":
                            last_60_month_meta["series"]\
                            if last_60_month_meta is not None else None,
                            "start_to_end_data":
                            last_60_month_meta["series"]\
                            if last_60_month_meta is not None else None,
                            "l_s_ratio_recent": l_s_ratio_recent,

                            "last_3_month_avg_l_s_ratio":
                            last_3_month_avg_l_s_ratio,
                            "last_6_month_avg_l_s_ratio":
                            last_6_month_avg_l_s_ratio,
                            "last_1_year_avg_l_s_ratio":
                            last_1_year_avg_l_s_ratio,
                            "last_3_year_avg_l_s_ratio":
                            last_3_year_avg_l_s_ratio,
                            "last_5_year_avg_l_s_ratio":
                            last_5_year_avg_l_s_ratio,

                            "curr_open_listings": curr_open_listings,

                            "curr_pending_sale": curr_pending_sale,

                            "last_3_month_total_txn": last_3_month_total_txn,
                            "last_6_month_total_txn": last_6_month_total_txn,
                            "last_1_year_total_txn": last_1_year_total_txn,
                            "last_3_year_total_txn": last_3_year_total_txn,
                            "last_5_year_total_txn": last_5_year_total_txn,

                            "last_3_month_avg_txn_per_week":
                            last_3_month_avg_txn_per_week,
                            "last_6_month_avg_txn_per_week":
                            last_6_month_avg_txn_per_week,
                            "last_1_year_avg_txn_per_week":
                            last_1_year_avg_txn_per_week,
                            "last_3_year_avg_txn_per_week":
                            last_3_year_avg_txn_per_week,
                            "last_5_year_avg_txn_per_week":
                            last_5_year_avg_txn_per_week,

                            "week_52_low": week_52_low,
                            "week_52_high": week_52_high,

                            "start_to_end_total_txs": last_5_year_total_txn,
                            "start_to_end_avg_txs_per_week":
                            last_5_year_avg_txn_per_week,
                            "start_to_end_avg_l_s_ratio":
                            last_5_year_avg_l_s_ratio,
                            })


class iZipStatusViewSet(LoggingMixin, viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def list(self, request):
        """
        iPrice Trend MLSLite ZipStatus

        It will returns the property types availabilty status of postalcodes.
        """
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        db_client.infodb.authenticate(**DATABASE_ACCESS)
        zip_status =\
            db_client['infodb']['mlslite_unique_data_zipstatus.s']\
            .find_one({"version": "v3"})['ministatus']

        return Response(zip_status)