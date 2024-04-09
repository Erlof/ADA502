import pymongo
import datetime
import logging
import json
from test_ting import time_format_now
# from database.conver_json import conver_to_json


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def convert_time(wd_data, loc):

    # wd_json_data = json.dumps(wd_data, indent=4, sort_keys=True, default=str)
    # print(type(wd_json_data))
    # print(wd_json_data)

    # wd_time = wd_json_data['time']
    # date_time = datetime.datetime.fromisoformat(wd_time)
    # wd_json_data['time'] = date_time

    for k in wd_data.copy():
        wd_data[str(k)]=wd_data.pop(k)
    #wd_json_data = json.dumps(wd_data, indent=4, sort_keys=True, default=str)

        
    wd_data_loc = {'loc' : loc} |  {'data': wd_data}
    
    return wd_data_loc





class mongo_connect:

    def __init__(self):
    
        # Connect to MongoDB
        Connection_string = "mongodb+srv://torgunnar1997:YdOKibc2YpOrZI6C@cluster0.w82ra9n.mongodb.net/"
        self.client = pymongo.MongoClient(Connection_string)
        db = self.client["database_fire_risks"]
        self.collection = db["fire_risks"]

    

    def upload(self, data):
        # Example: Insert a document
        
        self.collection.insert_one(data)


    def update(self, loc, data):

        self.collection.update_one(
            {'loc' : loc},
            {'$set' : {'data' : data}}
        )



    def chech_for_data(self, data):
        pathen = str(data)
        print(pathen)
        results = self.collection.find(
            )
        print(results, 'fant data')
        return results
    

    def disconnect(self):
        self.client.close()
        logging.info('Disconnected')



if __name__ == "__main__":

    loc_value = 60.383, 5.3327
    loc_str = str(loc_value)

    connect = mongo_connect()

    query = time_format_now()

    print('test')
    print(query)

    results = connect.chech_for_data(query)
    print(len(list(results)))

    for doc in list(results):
        print('Test')

