# Dynamisk Indikator for Brannfare

# Introduksjon
Dette prosjektet utnytter værprognoser og ob servasjonsdata for å beregne brannfare gjennom en tidsparameter kalt tid-til-full-overtenning (ttf) for trehus. Systemet analyserer innsendt geografisk posisjon og returnerer et gjennomsnitt av brannrisikoen i det angitte området.

# Arv og Utvikling
Repositoriet bygger på fundamentet av et foregående prosjekt og har blitt forbedret for å omfatte flere avanserte funksjoner. Prosjektet er utviklet av Erlend Lofthus og Tor Gunnar Hagen.

# Opprinnelig Prosjekt
Opprinnelige Utviklere: R.D. Strand og L.M. Kristensen
Tittel: Implementasjon, evaluering og validering av en dynamisk indikator for brann- og storbrannfare i trehus
Status: Under vurdering for publisering
Kilde: GitHub Repository

# Nye Funksjoner
En nytt API er implementert, som tillater brukere å angi geografiske koordinater (lengde- og breddegrad) gjennom følgende endepunkt: http://localhost:8000/compute-fire-risk?latitude=59.9139&longitude=10.7522. Systemet beregner og returnerer deretter et gjennomsnitt av brannrisikoen for det spesifikke området.

# Installasjon og Oppsett
Avhengigheter
Prosjektet bruker Poetry som pakkebehandler. Start installasjonen av Poetry ved å følge installasjonsinstruksjonene for Poetry. Opprett og aktiver et virtuelt miljø for å isolere avhengighetene:

```
poetry install
```

# Prosjektstruktur
Viktige Kataloger
Først frcm:
- `datamodel` - Definerer datastrukturene for vær- og brannfaredatamodeller.
- `weatherdata` Inneholder API-klienter og grensesnitt for å hente data fra eksterne værtjenester.
- `fireriskmodel` Implementerer den underliggende modellen for beregning av brannrisiko.
Hoved-APIet for dette systemet er implementert i filen `frcapi.py`

Så api:
- Denne delen hadde problemer med å kjøre fra main.py, så her ble det mye testing.
- `opend_data` blir brukt til å lese dataen rett

Siste katalog er database:
- På grunn av dårlig tid ble mesteparten her gjort i `test_mongodb`

# Integrerte Værdatakilder
Implementasjonen er designet for å være uavhengig av enhver spesifikk skybasert værdatatjeneste.

Dette biblioteket inneholder en implementasjon som bruker værdatatjenester levert av Meteorologisk institutt (MET).

Spesielt viser filene `src/frcm/weatherdata/client_met` and `src/frcm/weatherdata/extractor_met.py` hvordan man implementerer klienter og ekstraktorer ved å bruke:

MET Frost API for observasjoner av værdata: https://frost.met.no/index.html
MET Forecasting API for værdata-prognoser: https://api.met.no/weatherapi/locationforecast/2.0/documentation

For å bruke disse forhåndsimplementerte klientene må en fil med navn `.env` plasseres i mappen `src/frcm/weatherdata` som inneholder følgende innhold:

```
MET_CLIENT_ID = '<INSERT CLIENT ID HERE>'
MET_CLIENT_SECRET = '<INSERT CLIENT SECRET HERE>'
```
En '.env' fil må også bli laget i `src/database`. Denne er for å koble seg opp til mongodb. Hvis en ser på connection_string ser den ca. slik ut: "mongodb+srv://{MONGO_CLIENT}@{CLUSTER_ID}.mongodb.net/

```
MONGO_CLIENT_ID = '<INSERT CLIENT ID HERE>'
MONGO_CLIENT_SECRET = '<INSERT CLUSTER ID HERE>'

```

Legitimasjon for å bruke MET API-ene kan oppnås via: https://frost.met.no/auth/requestCredentials.html

Vennligst sørg for at du overholder vilkårene for bruk, som inkluderer begrensninger på antall API-kall.

# Testing
For å sikre funksjonaliteten til implementasjonen, utfør enhetstestene i katalogen tests med følgende kommando:

```
pytest
```

# Brukseksempler
Denne delen gir detaljerte eksempler på hvordan du kan interagere med systemet for å hente ut brannrisikovurderinger basert på geografiske koordinater.

Basis Bruk
For å kalkulere brannrisiko for en spesifikk lokasjon, benytt følgende format for API-endepunktet:


http://localhost:8000/compute-fire-risk?latitude=Breddegrad&longitude=Lengdegrad
Erstatt Breddegrad med ønsket breddegrad og Lengdegrad med ønsket lengdegrad. Dette vil sende en forespørsel til systemet som beregner og returnerer gjennomsnittlig brannrisiko for den angitte posisjonen basert på de nyeste tilgjengelige værdataene.

Her er ett eksempel hvis du ønsker og sjekke brannrisikoen til Hauegesund:
http://localhost:8000/compute-fire-risk?latitude=59.4138&longitude=5.2680

Da vil svaret se noe sånt ut:

```
["På dette området er firerisk [5.813460873150672] ved tidspunktet ['2024-04-16T11:00:00+00:00']",{}]
```
'{}' kommer fra et forsøk på å sende ut et plot av firerisks fremover, men dette ble ikke fullført i tide. 
