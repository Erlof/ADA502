# Dynamisk Indikator for Brannfare

## Introduksjon
Dette prosjektet utnytter værprognoser og observasjonsdata for å beregne brannfare gjennom en tidsparameter kalt tid-til-full-overtenning (ttf) for trehus. Systemet analyserer innsendt geografisk posisjon og returnerer brannrisikoen i det angitte området. En kan få brannrisikoen nå eller en graf av brannrisiko mot tid. Dette er gjort med å bruke FASTAPI og Mongodb, hvor FASTAPI ble brukt til å lage api-en som brukeren kan bruke og Mongodb ble brukt for å lage en database.

## Arv og Utvikling
Repetitoriet bygger på fundamentet av et foregående prosjekt og har blitt forbedret for å omfatte flere avanserte funksjoner. Prosjektet er utviklet av Erlend Lofthus og Tor Gunnar Hagen.

## Opprinnelig Prosjekt
Opprinnelige Utviklere: R.D. Strand og L.M. Kristensen
Tittel: Implementasjon, evaluering og validering av en dynamisk indikator for brann- og storbrannfare i trehus
Status: Under vurdering for publisering
Kilde: GitHub Repository

## Nye Funksjoner
En nytt API er implementert, som tillater brukere å angi geografiske koordinater (lengde- og breddegrad) gjennom følgende endepunkt: http://localhost:8000/compute-fire-risk?latitude=59.9139&longitude=10.7522. Her vil man motta brannrisikoen for det valgt område. 

I tillegg kan enn benytte endepunkt: http://localhost:8000/compute-fire-risk-graf?latitude=59.9139&longitude=10.7522. Da vil man motta en graf over brannrisikoen for valgt område.

Programmet bruker også mongodb for å lage dokumenter for de forskjellige posisjonene. Disse dokumentene har posisjon og et Dictionary med tidspunkt og brannrisiko. Disse er lagret slik at en kan fort få data fra en posisjon som er sjekket tidligere. Disse dokumentene blir oppdatert hvis de har gammel data. 

## Installasjon og Oppsett
Avhengigheter
Prosjektet bruker Poetry som pakkebehandler. Start installasjonen av Poetry ved å følge installasjonsinstruksjonene for Poetry. Opprett og aktiver et virtuelt miljø for å isolere avhengighetene:

```
poetry install
```

I tillegg må man opprette en mongodb bruker: https://www.mongodb.com/cloud/atlas/register

Docker kan installeres for å kjøre ett docker image istedenfor å kjøre lokalt på maskinen og benytte poetry. Docker desktop er anbefalt da det er lettere å jobbe med. 
https://docs.docker.com/engine/install/


## Prosjektstruktur
Viktige Kataloger

database:
- Databasen er delt opp i database_upload og test_mongodb. Der database_upload er ansvarlig for å laste opp data for å oppdatere mongodb og for å returnere data til api-en. Mens test_mongodb er ansvarlig for å kjøre selve databasen. 

frcm:
- datamodel - Definerer datastrukturene for vær- og brannfaredatamodeller.
- weatherdata - Inneholder API-klienter og grensesnitt for å hente data fra eksterne værtjenester.
- fireriskmodel - Implementerer den underliggende modellen for beregning av brannrisiko.
Hoved-APIet for dette systemet er implementert i filen frcapi.py

Disse henger sammen i main.py. Her startes api-en og en får værdata fra database eller fra frcm og det blir lagret i databasen.

## Integrerte Værdatakilder
Implementasjonen er designet for å være uavhengig av enhver spesifikk skybasert værdatatjeneste.

Dette biblioteket inneholder en implementasjon som bruker værdatatjenester levert av Meteorologisk institutt (MET).

Spesielt viser filene src/frcm/weatherdata/client_met and src/frcm/weatherdata/extractor_met.py hvordan man implementerer klienter og ekstraktorer ved å bruke:

MET Frost API for observasjoner av værdata: https://frost.met.no/index.html
MET Forecasting API for værdata-prognoser: https://api.met.no/weatherapi/locationforecast/2.0/documentation

For å bruke disse forhåndsimplementerte klientene må en fil med navn .env plasseres i mappen src/frcm/weatherdata som inneholder følgende innhold:

```
MET_CLIENT_ID = '<INSERT CLIENT ID HERE>'
MET_CLIENT_SECRET = '<INSERT CLIENT SECRET HERE>'
```

Legitimasjon for å bruke MET API-ene kan oppnås via: https://frost.met.no/auth/requestCredentials.html

Vennligst sørg for at du overholder vilkårene for bruk, som inkluderer begrensninger på antall API-kall.


Mongodb:
En '.env' fil må også bli laget i src/database. Denne er for å koble seg opp til mongodb. Hvis en ser på connection_string ser den ca. slik ut: 
mongodb+srv://{MONGO_CLIENT}@{CLUSTER_ID}.mongodb.net/»

```
MONGO_CLIENT_ID = '<INSERT CLIENT ID HERE>'
MONGO_CLIENT_SECRET = '<INSERT CLUSTER ID HERE>'
```


## Testing
For å sikre funksjonaliteten til implementasjonen, utfør enhetstestene i katalogen tests med følgende kommando:

```
pytest
```

På grunn av feil med unittest kunne vi dessverre ikke lage automatiske tester for alle tingene vi ville teste. 
## Brukseksempler
Dette er 2 muligheter for å motta brannrisikoen i ett område:

- Nummer 1:
Denne delen gir detaljerte eksempler på hvordan du kan interagere med systemet for å hente ut brannrisikovurderinger basert på geografiske koordinater.

Basis Bruk
For å kalkulere brannrisiko for en spesifikk lokasjon, benytt følgende format for API-endepunktet:
http://localhost:8000/compute-fire-risk?latitude=Breddegrad&longitude=Lengdegrad
Erstatt Breddegrad med ønsket breddegrad og Lengdegrad med ønsket lengdegrad. Dette vil sende en forespørsel til systemet som beregner og returnerer brannrisiko for den angitte posisjonen basert på de nyeste tilgjengelige værdataene.

Her er ett eksempel hvis du ønsker å sjekke brannrisikoen til Haugesund:
http://localhost:8000/compute-fire-risk?latitude=59.4138&longitude=5.2680

Da vil svaret se noe sånt ut:

"På dette området er firerisk [6.576648704266775] ved tidspunktet ['2024-05-14T20:00:00+00:00']"

- Nummer 2:
Ved å benytte:
http://localhost:8000/compute-fire-risk-graf?latitude=Breddegrad&longitude=Lengdegrad
Erstatt Breddegrad med ønsket breddegrad og Lengdegrad med ønsket lengdegrad. Dette vil sende en forespørsel til systemet som returner en graf over brannrisikoen de over en bestemt periode.

Her er ett eksempel hvis du ønsker å sjekke brannrisikoen til Haugesund:
http://localhost:8000/compute-fire-risk-graf?latitude=59.4138&longitude=5.2680

Det er også mulig å kjørde den i bare lokalhost. For å gjøre dette skriver en:
http://127.0.0.1:8000/
Her får en opp en liten tekst som forteller om alternativ 1 og 2.


## Docker
Det er også mulig å lage et docker image og containers. For å gjøre dette kan en kjøre filen Dockerfile med docker. Dette gjør en med å kjøre:

```
docker build -f  .\Dockerfile -t fire-risk-image .
```

Dette må gjøres i mappen med Dockerfile. Dette lager et image som heter ‘fire-risk-image’. For å kjøre fire-risk-image kan en gjøre dette i docker desktop eller med å kjøre:

```
docker run -p 8000:8000 --name container_fire_risk fire-risk-image
```

Da blir det startet en container som heter ‘container_fire_risk’. Legg merke til at her sørger en for at porten 8000 blir brukt til api-en, slik som å kjøre main.py. For å gjøre det samme ved å kjøre det i docker desktop må en fortelle docker desktop hvilken port en vil kjøre. 

Det er også mulig å kjøre med å bruke docker-compose filen. For å gjøre det bruk disse komandoene:

```
docker compose build

docker compose up
```
