from scipy import stats
import numpy as np
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import enum
import datetime
import calendar
from pymongo import MongoClient
import statistics
from pyzipcode import Pyzipcode as pz
# from django.shortcuts import render
# from django.http import HttpResponseRedirect


class TrendType(enum.Enum):
    WEEKLY = 'week'
    MONTHLY = 'month'
    YEARLY = 'year'


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


@permission_classes((permissions.AllowAny,))
class iPriceTrendViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        iPrice Trend Version beta version .

         It will  get the input as postalcode and response data is in monthly format(if span is year) as well as weekly (if span is month ).

         url:https://insights.propmix.io:8006/iprice/trend

        ---
        # YAML (must be separated by `---`)

        type:
          zipcode:
            required: true
            type: string
          type:
            required: false
            type: string

        parameters:
            - name: zip
              description: Postalcode which iPriceTrend to be calculated.
              required: true
              type: string
              paramType: query
              defaultValue: 33134


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
        except:
            return Response({'status': 'ERROR', 'error': 'NO_ZIP_SPECIFIED'})
        db_client = MongoClient('mongo-master.propmix.io', 33017)
        # hive_driver = HiveDriver(database='iprice', host='hadoop-master.propmix.io', port=10000, user='hue')
        now = datetime.datetime.now()
        zipcode = pz.get[int(request.query_params['zip']), "US"]
        zip_code_location = ', '.join([zipcode['county'], zipcode['state_short']])

        aggregation_pipeline_6M = [{"$match": {"postalcode": str(request.query_params['zip']),
                                               "closedate": {"$gte": monthdelta(now, -6).strftime('%Y-%m-%d')},
                                               "closeprice": {"$ne": None}
                                               }
                                    },
                                   {"$group": {"_id": {"week": "$week", "year": "$year"},
                                               "price_sqft": {"$push": "$price_sqft"},
                                               "count": {"$sum": 1}}},
                                   {"$sort": {"_id.year": 1, "_id.week": 1}}]
        aggregation_pipeline_5Y = [{"$match": {"postalcode": str(request.query_params['zip']),
                                               "closedate": {"$gte": monthdelta(now, -12 * 5).strftime('%Y-%m-%d')},
                                               "closeprice": {"$ne": None}
                                               }},
                                   {"$group": {"_id": {"month": "$month", "year": "$year"},
                                               "price_sqft": {"$push": "$price_sqft"},
                                               "count": {"$sum": 1}}},
                                   {"$sort": {"_id.year": 1, "_id.month": 1}}]

        aggregation_pipeline_ls_5Y = [{"$match": {"postalcode": str(request.query_params['zip']),
                                                  "closedate": {"$gte": monthdelta(now, -12 * 5).strftime('%Y-%m-%d')},
                                                  "closeprice": {"$ne": None}
                                                  }},
                                      {"$group": {"_id": {"week": "$week", "year": "$year"},
                                                  "lsratio": {"$push": "$lsratio"},
                                                  "count": {"$sum": 1}}},
                                      {"$sort": {"_id.year": 1, "_id.week": 1}}]

        data_6M = list(db_client.ipricetrend.iprice.aggregate(aggregation_pipeline_6M))
        data_5Y = list(db_client.ipricetrend.iprice.aggregate(aggregation_pipeline_5Y))
        data_ls_5Y = list(db_client.ipricetrend.iprice.aggregate(aggregation_pipeline_ls_5Y))

        last_3_month_data, series_3M = self.get_data_(data_6M[-12:], TrendType.WEEKLY)
        last_6_month_data, _series_6M = self.get_data_(data_6M, TrendType.WEEKLY)

        last_1_year_data, series_1Y = self.get_data_(data_5Y[-12:], TrendType.MONTHLY)
        last_3_year_data, _series_3Y = self.get_data_(data_5Y[-36:], TrendType.MONTHLY)
        last_5_year_data, _series_5Y = self.get_data_(data_5Y, TrendType.MONTHLY)

        week_52_high = max(series_1Y)
        week_52_low = min(series_1Y)

        ls_series, txn_series = self.get_ls_txn_series(data_ls_5Y)

        l_s_ratio_recent = (ls_series[-1]) * 100.0
        last_3_month_avg_l_s_ratio = (sum(ls_series[-12:]) / 12.0) * 100.0
        last_6_month_avg_l_s_ratio = (sum(ls_series[-24:]) / 24.0) * 100.0
        last_1_year_avg_l_s_ratio = (sum(ls_series[-52:]) / 52.0) * 100.0
        last_3_year_avg_l_s_ratio = (sum(ls_series[-52 * 3:]) / (52.0 * 3.0)) * 100.0
        last_5_year_avg_l_s_ratio = (sum(ls_series[-52 * 5:]) / (52.0 * 5.0)) * 100.0

        last_3_month_total_txn = sum(txn_series[-12:])
        last_6_month_total_txn = sum(txn_series[-24:])
        last_1_year_total_txn = sum(txn_series[-52:])
        last_3_year_total_txn = sum(txn_series[-52 * 3:])
        last_5_year_total_txn = sum(txn_series[-52 * 5:])

        last_3_month_avg_txn_per_week = sum(txn_series[-12:]) / 12.0
        last_6_month_avg_txn_per_week = sum(txn_series[-24:]) / 24.0
        last_1_year_avg_txn_per_week = sum(txn_series[-52:]) / 52.0
        last_3_year_avg_txn_per_week = sum(txn_series[-52 * 3:]) / (52.0 * 3.0)
        last_5_year_avg_txn_per_week = sum(txn_series[-52 * 5:]) / (52.0 * 5.0)

        reference = range(1, len(series_3M) + 1)
        data = np.asarray(series_3M)

        reference = np.asarray(reference)
        x = reference
        y = data
        slope, intercept, _r_value, _p_value, _std_err = stats.linregress(x, y)
        pps0 = intercept
        ppsn = slope * 11 + intercept

        price_per_square_feet = ppsn
        last_3_months_trend_variation = ppsn - pps0
        last_3_months_price_trend_percentage = (float(ppsn - pps0) / float(pps0)) * 100.0
        last_3_months_price_trend_change = '+' if last_3_months_trend_variation >= 0 else '-'
        # print datetime.datetime.now()
        return Response({'slope': slope,
                         'intercept': intercept,
                         "zip_code_location": zip_code_location,
                         "price_per_square_feet": price_per_square_feet,
                         "last_3_months_trend_variation": last_3_months_trend_variation,
                         "last_3_months_price_trend_percentage": last_3_months_price_trend_percentage,
                         "last_3_months_price_trend_change": last_3_months_price_trend_change,
                         "last_3_month_data": last_3_month_data,
                         "last_6_month_data": last_6_month_data,
                         "last_1_year_data": last_1_year_data,
                         "last_3_year_data": last_3_year_data,
                         "last_5_year_data": last_5_year_data,
                         "l_s_ratio_recent": l_s_ratio_recent,
                         "last_3_month_avg_l_s_ratio": last_3_month_avg_l_s_ratio,
                         "last_6_month_avg_l_s_ratio": last_6_month_avg_l_s_ratio,
                         "last_1_year_avg_l_s_ratio": last_1_year_avg_l_s_ratio,
                         "last_3_year_avg_l_s_ratio": last_3_year_avg_l_s_ratio,
                         "last_5_year_avg_l_s_ratio": last_5_year_avg_l_s_ratio,
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
                         "week_52_high": week_52_high
                         })
#         return Response({'slope':slope, 'intercept':intercept, 'zip':zip, 'span':span})

    def get_ls_txn_series(self, table):
        ls_series = []
        txn_series = []
        for item in table:
            ls_series.append(float(statistics.median(item['lsratio'])))
            txn_series.append(float(item['count']))
        return ls_series, txn_series

    def get_data_(self, data, rtype):
        last_x_rtype_periods = []
        last_x_rtype_ppsf = []
        last_x_rtype_vnos = []
        series = []
        week_cache = None
        year_cache = None
        for item in data:
            date_str = '01/01/2010'
            wday = 0
            if rtype is TrendType.WEEKLY:
                if week_cache is not None and week_cache == int(item["_id"]["week"]) and year_cache == int(item["_id"]["year"]):
                    wday = 0
                    print week_cache, 'cache match'
                else:
                    wday = 1
                week_cache = int(item["_id"]["week"])
                year_cache = int(item["_id"]["year"])
                date_str = datetime.datetime.strptime(str(item["_id"]["year"]) + '-' + str(item["_id"]["week"]) + '-' + str(wday), "%Y-%W-%w").strftime("%d/%m/%Y")
            else:
                day = calendar.monthrange(int(item["_id"]["year"]), int(item["_id"]["month"]))[1]
                date_str = datetime.datetime.strptime(str(item["_id"]["year"]) + '-' + str(item["_id"]["month"]) + '-' + str(day), "%Y-%m-%d").strftime("%d/%m/%Y")
            last_x_rtype_periods.append({"label": date_str})
            last_x_rtype_ppsf.append({"value": float(statistics.median(item["price_sqft"]))})
            last_x_rtype_vnos.append({"value": int(item["count"])})
            series.append(last_x_rtype_ppsf[-1]['value'])
        last_x_rtype_data = [{"periods": last_x_rtype_periods}, {"price_per_square_feet": last_x_rtype_ppsf}, {"volume_num_of_sales": last_x_rtype_vnos}]
        return last_x_rtype_data, series

    def get_data(self, table, span, rtype):
        last_x_rtype_periods = []
        last_x_rtype_ppsf = []
        last_x_rtype_vnos = []
        series = []
        week_cache = None
        year_cache = None
        for item in table:
            date_str = '01/01/2010'
            wday = 0
            if rtype is TrendType.WEEKLY:
                if week_cache is not None and week_cache == int(item[0]) and year_cache == int(item[2]):
                    wday = 0
                    print week_cache, 'cache match'
                else:
                    wday = 1
                week_cache = int(item[0])
                year_cache = int(item[2])
                date_str = datetime.datetime.strptime(str(item[2]) + '-' + str(item[0]) + '-' + str(wday), "%Y-%W-%w").strftime("%d/%m/%Y")
            else:
                day = calendar.monthrange(int(item[2]), int(item[1]))[1]
                date_str = datetime.datetime.strptime(str(item[2]) + '-' + str(item[1]) + '-' + str(day), "%Y-%m-%d").strftime("%d/%m/%Y")
            last_x_rtype_periods.append({"label": date_str})
            last_x_rtype_ppsf.append({"value": float(item[-2])})
            last_x_rtype_vnos.append({"value": int(item[-1])})
            series.append(float(item[-2]))
        last_x_rtype_data = [{"periods": last_x_rtype_periods}, {"price_per_square_feet": last_x_rtype_ppsf}, {"volume_num_of_sales": last_x_rtype_vnos}]
        return last_x_rtype_data, series


# from .forms import NameForm
#
#
# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request,  'name.html', {'form': form})
