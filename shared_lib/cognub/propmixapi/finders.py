'''
Created on May 12, 2016

@author: joseph
'''
import numpy as np

def find_median_vector(vector_list):
    if type(vector_list) is list:
        np_ndvector = np.asarray(vector_list, dtype="double")
    else:
        np_ndvector = vector_list
    median_vector = np.median(np_ndvector, axis=0)
    return median_vector

def find_mean_vector(vector_list):
    if type(vector_list) is list:
        np_ndvector = np.asarray(vector_list, dtype="double")
    else:
        np_ndvector = vector_list
    median_vector = np.mean(np_ndvector, axis=0)
    return median_vector