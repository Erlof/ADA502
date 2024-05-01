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

from database.database_upload import get_data_graf, get_data_now

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

        data = get_data_now(loc_str, location, frc)

        return f'På dette området er firerisk {list(data.values())} ved tidspunktet {list(data.keys())}'



    @app.get("/compute-fire-risk-graf")
    def compute_fire_risk_graf(latitude: float, longitude: float):
    
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

        bufContents = get_data_graf(loc_str, location, frc)

        headers = {'Content-Disposition': 'inline; filename="out.png"'}

        return Response(bufContents, headers = headers, media_type='image/jpeg')

    uvicorn.run(app, host="0.0.0.0", port=8000)

