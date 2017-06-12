from pymongo import MongoClient

db_client = MongoClient(host='169.45.215.122', port=33017)
data_= list(db_client["iestimate"]["HeatMapMediansCountyWise_copy"].find({}, {'1Y.ListPrice':True,"coordinates":True}))
feture_data_List=[]

for i in range(len(data_))  :
    try:
        County=data_[i]['_id']['County']
        Heat5y=data_[i]['1Y']['ListPrice'];
        prop={'County':County,'ListPrice':Heat5y}
        print i, data_[i]['_id']['County'], data_[i]['coordinates']
        cords=data_[i]['coordinates']
        polygon={'type':'Polygon','coordinates':cords}
        feture_data_List.append({'type':'1Y','id':i,'properties':prop,'geometry':polygon})
    except: 
        print 'nodata for County',  County  
calc = {'type':"FeatureCollection",'features':feture_data_List}

