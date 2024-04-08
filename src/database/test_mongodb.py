import pymongo
import datetime
import logging
import json
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

        
    wd_data_loc = {loc: wd_data}
    
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

    def chech_for_data(self, loc, data):
        pathen = str(loc)+'.'+str(data)
        print(pathen)
        results = self.collection.find(
            { pathen : {"$exists":True} }
            )
        return results


    def get_data(self,loc,  query):
        # Example: Query documents
        results = self.chech_for_data(loc, query)

        return results

    def disconnect(self):
        self.client.close()
        logging.info('Disconnected')



if __name__ == "__main__":
    data = {"name": "Pizza Palace", "cuisine": "Italian"}
    query = {"cuisine": "Italian"}
    
    connect = mongo_connect()
    connect.upload(data = data)
    connect.get_data(query = query)
    connect.disconnect()
