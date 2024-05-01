import pymongo
import datetime
import logging
import json
from test_ting import time_format_now
# from database.conver_json import conver_to_json
import matplotlib.pylab as plt
import matplotlib 
matplotlib.use('AGG')
import io
from frcm.datamodel.model import Location

# see .env.example.py in the root dir.
from decouple import config


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def convert_time(wd_data, loc):


    for k in wd_data.copy():
        wd_data[str(k)]=wd_data.pop(k)

        
    wd_data_loc = {'loc' : loc} |  {'data': wd_data}
    
    return wd_data_loc





class mongo_connect:

    def __init__(self):

        self.MONGO_CLIENT = config('MONGO_CLIENT_ID')
        self.MONGO_server = config('MONGO_CLIENT_SECRET')

    
        # Connect to MongoDB
        Connection_string = f"mongodb+srv://{self.MONGO_CLIENT}@{self.MONGO_server}.mongodb.net/"
        self.client = pymongo.MongoClient(Connection_string)
        db = self.client["database_fire_risks"]
        self.collection = db["fire_risks"]

    

    def upload(self, data):
        # Example: Insert a document
        self.collection.insert_one(data)


    def update(self, loc, data):
        print('Updates the database for', loc)

        count = self.collection.count_documents({'loc' : loc})

        if count == 0:
            self.upload(
                data
                )
        
        else:
            self.collection.update_one(
                {'loc' : loc},
                {'$set' : {'data' : data['data']}}
            )



    def chech_for_data(self, loc, data):
        data_path = str(data)
        loc_path = str(loc)
        results = self.collection.find({'loc':loc_path, f'data.{data_path}': {"$exists" : 'true'}}, {f'data.{data_path}': 1})
        return results
    

    def all_data_fra_loc(self, loc):
        pathen = str(loc)
        results = self.collection.find({'loc' : pathen}, {'data' : 1})
        return results
    
    
    def make_plot(self, loc, img_buf):

        results = self.all_data_fra_loc(loc)

        for doc in results:
            data = doc['data']
        # print('Data for plot\n', data)
        
        lists = sorted(data.items()) # sorted by key, return a list of tuples

        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.rcParams['figure.figsize'] = [10, 7]
        plt.rcParams['figure.autolayout'] = True
        fig = plt.figure()
        plt.plot(x, y)
        plt.xticks([x[0], x[-1]], visible=True)
        plt.xlabel('Tid')
        plt.ylabel('Fire risk')
        plt.title(str(loc))
        plt.savefig(img_buf, format='JPEG')
        img_buf.seek(0)
        bufContents: bytes = img_buf.getvalue()


        return bufContents
        

    def disconnect(self):
        self.client.close()
        logging.info('Disconnected')



if __name__ == "__main__":

    latitude, longitude = 60.383, 5.3327
    location = Location(latitude=latitude, longitude=longitude)

    loc_value = location.latitude, location.longitude
    loc_str = str(loc_value)

    connect = mongo_connect()

    query = time_format_now()

    print('test')
    print(query)


    bilde = connect.make_plot(loc_str)
    


    connect.disconnect()


