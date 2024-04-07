import datetime
import logging

from frcm.frcapi import FireRiskAPI
from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor
from frcm.datamodel.model import Location
from fastapi import FastAPI, HTTPException, Query


app = FastAPI()

# Sett opp logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Opprett METClient og FireRiskAPI-objekter
met_extractor = METExtractor()
met_client = METClient(extractor=met_extractor)
frc = FireRiskAPI(client=met_client)







    # Koden under her, sender bare lokasjon og får svar ut ifra dette.




# Funksjon for å beregne brannrisiko basert på lokasjon
@app.get("/compute-fire-risk")
def compute_fire_risk(latitude: float, longitude: float):
    try:
        # Logg mottatt lokasjon
        logger.info(f"Received latitude: {latitude}, longitude: {longitude}")

        # Print both latitude and longitude in PyCharm
        print("Received latitude:", latitude)
        print("Received longitude:", longitude)

        # Opprett Location-objekt basert på mottatt bredde- og lengdegrad
        location = Location(latitude=latitude, longitude=longitude)

        # Hent brannrisikoprediksjoner for lokasjonen
        obs_delta = datetime.timedelta(days=1)
        predictions = frc.compute_now(location, obs_delta)
        #print("Dette er brannrisikoen", predictions)
       # print( predictions)
       # print( predictions)

        # Definer funksjonen for å hente brannrisiko

        # Kall get_fire_risk funksjonen og skriv ut verdien av tall og gjennomsnitt
        #tall_verdi, gjennomsnitt_verdi = get_fire_risk(predictions)
        #print("Verdien av tall er:", tall_verdi)
        #print("Gjennomsnittet av tallene er:", gjennomsnitt_verdi)

        # Kall get_fire_risk funksjonen for å beregne gjennomsnittet av tallene
        tall_verdi, gjennomsnitt_verdi = get_fire_risk(predictions)
        logger.info(f"Tall verdi: {tall_verdi}, Gjennomsnitt verdi: {gjennomsnitt_verdi}")

        # Returner gjennomsnittet av tallene som et svar
        return {"Gjennomsnitt verdien for brannrisikoen i dette området er": gjennomsnitt_verdi}

        # Velg brannrisikoen fra prediksjonene
        #fire_risk = predictions["fire_risk"]




        # Returner brannrisiko
        #return {"fire_risk": fire_risk}


    except Exception as e:
        logger.error(f"Error occurred while computing fire risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))


 # Definer funksjonen for å hente brannrisiko
def get_fire_risk(predictions):
    tall = []
    for lines in predictions.firerisks:
        tall.append(lines.ttf)
    # Beregn gjennomsnittet av tallene
    gjennomsnitt = sum(tall) / len(tall)


    return tall, gjennomsnitt

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
