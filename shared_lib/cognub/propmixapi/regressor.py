'''
Created on May 12, 2016

@author: joseph
'''
from sklearn.linear_model import LinearRegression, RidgeCV, Ridge
from sklearn.svm import SVR
from pymongo import MongoClient
from cognub.propmixapi.preprocessors import mongo_dsto_nparray,\
    mongo_dsto_norm_nparray
from cognub.propmixapi.datasets.featuresconf import features_regression_model
import pickle
from cognub.propmixapi.finders import find_median_vector
import datetime
import numpy as np

db_client = MongoClient('169.45.215.122', 33017)

dataset = db_client.iestimate.predictions81k_ecp.find({"postalcode":"01720"})

features_list, target_list = mongo_dsto_nparray(dataset, features_regression_model)
regression_model = LinearRegression(normalize=False)
print regression_model.fit(features_list, target_list).score(features_list, target_list)
print regression_model.get_params()
pickle.dump(regression_model, open("sklearn.linear_regression.model", "w"))
for index in range(10):
    print regression_model.predict(features_list[index].reshape(1,-1)), target_list[index]
median_vector =  find_median_vector(features_list)
median_vector[3] = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds()
print regression_model.predict(median_vector.reshape(1,-1))
print median_vector
import matplotlib.pyplot as plt
import copy
x = []
y = []
for year in range(2010,2016):
    for month in range(1, 13):
        x.append((year-2010)*12 + month)
        median_vector[3] = (datetime.datetime(year, month, 1) - datetime.datetime(1970, 1, 1)).total_seconds()
        y.append(regression_model.predict(copy.deepcopy(median_vector).reshape(1,-1)))
plt.plot(x, y)
plt.show()
