'''
Created on 18-Aug-2016

@author: revathy.sivan
'''
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
x=pd.read_csv('/home/revathy.sivan/Desktop/prop_mix data/best_fit_data.csv')
xx=x.ix[:,0:9]

x1=xx.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
x11=x1.as_matrix()
x1=x11.astype(float)
valid = np.isfinite(x1)
mu = np.nanmean(x1, 0, keepdims=1)
X_hat = np.where(valid, x1, mu)
for ii in range(10):
    cls = KMeans(n_clusters=10, n_jobs=1)
    labels_hat = cls.fit_predict(X_hat)
    X_hat[~valid] = cls.cluster_centers_[labels_hat][~valid]
x2= X_hat
x2=pd.DataFrame(x2) 
x2.columns = ['Distance','LotSizeArea','GLA','beds','baths','garage','viewyn','ParkingTotal','YearBuilt']
#x1 = x1.replace("[+]", "",regex=True)
#x1=x1.replace(['One Story'],[1])
#mean=[0,7350,1420,3,3,0,1,1,1953]
c=x2.append({'Distance':0,'LotSizeArea':7350,'GLA':1420,'beds':3,'baths':3,'garage':5,'viewyn':0,'ParkingTotal':5,'YearBuilt':1953},ignore_index='true')
subject=c.tail(1)
d=len(c.index)
mean=c.loc[d-1]
mean = np.array(mean, dtype='int32').tolist()
l=len(c.columns)
c.columns=[range(l)]
c=c.convert_objects(convert_numeric=True) 
for index  in range(len(c.columns)):   
    c[index]=abs(mean[index]-c[index])
mR=c.apply(lambda dh: np.sum(dh), axis=1)
c['similarity_score']=mR
c=c.sort(['similarity_score'], ascending=1)
c=c.reset_index(level=0)
#newinput=x.append(subject)
#
#x=newinput
x['similarity_score']=mR
x=x.sort(['similarity_score'], ascending=[True])
x=x.reset_index(level=0)
Topten_similar_property=x[:10]

Best_fit_agent=Topten_similar_property.iloc[0]['Agent_name']
print Best_fit_agent




