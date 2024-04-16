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
        
    app = FastAPI()

    @app.get("/compute-fire-risk")
    def compute_fire_risk(latitude: float, longitude: float):

        print("Received latitude:", latitude)
        print("Received longitude:", longitude)


        met_extractor = METExtractor()

        # TODO: maybe embed extractor into client
        met_client = METClient(extractor=met_extractor)

        frc = FireRiskAPI(client=met_client)


        location = Location(latitude=latitude, longitude=longitude)
        # location = Location(latitude=60.383, longitude=5.3327)  # Bergen

        loc_str = met_client.get_nearest_station_id(location)

        print('Connencts to mongo')
        connect = mongo_connect()

        query = time_format_now()
        

        results = connect.chech_for_data(loc_str, query)
        ct = 0

        for doc in results:

            print(doc)
            data = doc['data']
            ct += 1



        if ct == 0:
            print('Updaterer data for å få ny data')

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

        img_buf = connect.make_plot(loc_str)

        print('disconnects from mongo')

        connect.disconnect()

        img_buf.seek(0)

        return {f'På dette området er firerisk {list(data.values())} ved tidspunktet {list(data.keys())}',
                img_buf}
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

