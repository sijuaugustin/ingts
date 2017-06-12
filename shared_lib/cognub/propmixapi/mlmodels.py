'''
Created on May 12, 2016

@author: joseph
'''
from pyspark import SparkContext
from pyspark import SQLContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel
from pymongo import MongoClient
from cognub.propmixapi.datasets.featuresconf import features_regression_model
from cognub.propmixapi.preprocessors import dsto_labeled_points,\
    dsto_norm_labeled_points

sc = SparkContext()

sql_context = SQLContext(sc)

db_client = MongoClient('169.45.215.122', 33017)

dataset = db_client.iestimate.predictions81k_ecp_copy.find({"postalcode":"01772"})

dataset = dsto_norm_labeled_points(dataset, features_regression_model)

dataset = sc.parallelize(dataset)



# Load and parse the data
# def parsePoint(line):
#     values = [float(x) for x in line.replace(',', ' ').split(' ')]
#     return LabeledPoint(values[0], values[1:])
# 
# data = sc.textFile("data/mllib/ridge-data/lpsa.data")
# parsedData = data.map(parsePoint)
processed_data = dataset

# Build the model
model = LinearRegressionWithSGD.train(processed_data, iterations=300, step=0.01)

# Evaluate the model on training data
valuesAndPreds = processed_data.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))

# Save and load model
model.save(sc, "myModelPath")
sameModel = LinearRegressionModel.load(sc, "myModelPath")