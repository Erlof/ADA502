import datetime 
from fastapi import FastAPI
import uvicorn

from frcm.frcapi import FireRiskAPI
from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor
from frcm.datamodel.model import Location
from api.uploads_data import api_fast
from api.uploads_data import get_fire_risk
from database.test_mongodb import mongo_connect
from database.test_mongodb import convert_time
from test_ting import time_format_now

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":

    met_extractor = METExtractor()

    # TODO: maybe embed extractor into client
    met_client = METClient(extractor=met_extractor)

    frc = FireRiskAPI(client=met_client)

    # location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    location = Location(latitude=59.4225, longitude=5.2480)  # Haugesund

    # Fails
    # location = Location(latitude=62.5780, longitude=11.3919)  # Røros
    # location = Location(latitude=69.6492, longitude=18.9553)  # Tromsø

    loc_value = location.latitude, location.longitude
    loc_str = str(loc_value)

    connect = mongo_connect()

    query = time_format_now()
    
    print('test')
    print(query)

    results = connect.get_data(loc_str, query)
    #print(results.pretty())
    

    if results == None:


        # how far into the past to fetch observations

        obs_delta = datetime.timedelta(days=1)

        predictions = frc.compute_now(location, obs_delta)
        

        # print(predictions)

        firerisks = get_fire_risk(predictions)
        #print(firerisks)
        # api_fast.make_file(firerisks)
        
        pred_formatted = convert_time(firerisks, loc_str)

        # print(pred_formatted)

        connect.upload(data = pred_formatted)
        
        results = connect.get_data(loc_str, query = query)
        for doc in results:
            print(doc)

    else:
        for doc in results:
            print(doc)



    connect.disconnect()


    app = FastAPI()

    # Funker ikke fra api.da
    @app.get("/")
    def root():
        return {"message": firerisks}
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

