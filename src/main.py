import datetime 
from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
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


app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def fikk_ingenting():
    return 'For å få firerisk bruk:\nhttp://localhost:8000/compute-fire-risk?latitude=Breddegrad&longitude=Lengdegrad \nErstatt Breddegrad med ønsket breddegrad og Lengdegrad med ønsket lengdegrad. Dette vil sende en forespørsel til systemet som beregner og returnerer gjennomsnittlig brannrisiko for den angitte posisjonen basert på de nyeste tilgjengelige værdataene. Her er ett eksempel hvis du ønsker og sjekke brannrisikoen til Hauegesund: http://localhost:8000/compute-fire-risk?latitude=59.4138&longitude=5.2680 \nHvis en vil ha en graf så kan en bruke: \nhttp://localhost:8000/compute-fire-risk-graf?latitude=Breddegrad&longitude=Lengdegrad'
    


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

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":
        
    uvicorn.run(app, host="0.0.0.0", port=8000)

