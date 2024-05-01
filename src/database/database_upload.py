import datetime
from fastapi import FastAPI, Response
import uvicorn
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import io 

from frcm.frcapi import FireRiskAPI
from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor
from frcm.datamodel.model import Location
from api.uploads_data import api_fast
from api.uploads_data import get_fire_risk
from database.test_mongodb import mongo_connect
from database.test_mongodb import convert_time
from test_ting import time_format_now


def get_data_now(loc_str, location, frc):

    connect = mongo_connect()

    query = time_format_now()
    
    results = connect.chech_for_data(loc_str, query)
    ct = 0

    print('Sjekker om det er oppdatert data.')

    results.rewind()

    for doc in results:

        print('Fant data')
        print(doc)
        data = doc['data']
        ct += 1


    if ct == 0:
        print('Updaterer mongodb for å få ny data')

        # how far into the past to fetch observations

        obs_delta = datetime.timedelta(days=1)

        predictions = frc.compute_now(location, obs_delta)
        

        # print(predictions)

        firerisks = get_fire_risk(predictions)
        #print(firerisks)
        # api_fast.make_file(firerisks)
        
        pred_formatted = convert_time(firerisks, loc_str)

        # print(pred_formatted)

        connect.update(loc = loc_str, data = pred_formatted)
        
        results = connect.chech_for_data(loc_str, query)

            
        for doc in results:

            print(doc)
            data = doc['data']

    return data

def get_data_graf(loc_str, location, frc):

    connect = mongo_connect()

    query = time_format_now()
    
    results = connect.chech_for_data(loc_str, query)
    ct = 0

    print('Sjekker om det er oppdatert data.')

    results.rewind()

    for doc in results:

        print('Fant data')
        print(doc)
        ct += 1


    if ct == 0:
        print('Updaterer mongodb for å få ny data')

        # how far into the past to fetch observations

        obs_delta = datetime.timedelta(days=1)

        predictions = frc.compute_now(location, obs_delta)
        

        # print(predictions)

        firerisks = get_fire_risk(predictions)
        #print(firerisks)
        # api_fast.make_file(firerisks)
        
        pred_formatted = convert_time(firerisks, loc_str)

        # print(pred_formatted)

        connect.update(loc = loc_str, data = pred_formatted)
        
    with io.BytesIO() as img_buf:
            
        bufContents = connect.make_plot(loc_str, img_buf)

        return bufContents

    return data












# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":

    met_extractor = METExtractor()

    # TODO: maybe embed extractor into client
    met_client = METClient(extractor=met_extractor)

    frc = FireRiskAPI(client=met_client)

    #location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    location = Location(latitude=59.4225, longitude=5.2480)  # Haugesund


    loc_value = location.latitude, location.longitude
    loc_str = str(loc_value)

    connect = mongo_connect()

    query = time_format_now()
   

    # how far into the past to fetch observations

    obs_delta = datetime.timedelta(days=1)

    predictions = frc.compute_now(location, obs_delta)
    

    firerisks = get_fire_risk(predictions)
    #print(firerisks)
    # api_fast.make_file(firerisks)
    
    pred_formatted = convert_time(firerisks, loc_str)

    # print(pred_formatted)

    connect.upload(data = pred_formatted)