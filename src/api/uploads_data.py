from fastapi import FastAPI
import uvicorn
import datetime


def get_fire_risk(predictions):
    # Want them in a dict
    tall = []
    tid = []
    for lines in predictions.firerisks:
        tall.append(lines.ttf)
        tid.append(lines.timestamp.isoformat())

    dictionary = dict(zip(tid, tall))

    return dictionary

class api_fast:

    def __init__(self):
        self.app = FastAPI()



    def open_fast_api(tall):


        @self.app.get("/")
        def root():
            return {"message": tall}

    def make_file(tall):
    
        with open("position.txt", "w") as fil:
            fil.write(str(tall))
        print(fil.closed)

        

        
if __name__ == "__main__":

    tall = [1, 2, 3]

    test_api = api_fast()

    test_api.open_fast_api(tall)
    uvicorn.run(app, host="0.0.0.0", port=8000)
