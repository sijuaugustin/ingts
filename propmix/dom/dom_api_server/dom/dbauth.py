'''
Created on Feb 17, 2017

@author: vivek.mv
'''
DATABASE_ACCESS = {'name': 'dom_api',
                   'password': 'domapi#98',
                   'source': 'cognubauth'
                   }
                   
'''USAGE: 
        from pymongo import MongoClient
        from .dbauth import DATABASE_ACCESS
        dbclient = MongoClient(host, port)
        dbclient.specificdatabase.authenticate(**DATABASE_ACCESS)
'''
