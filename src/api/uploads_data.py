from fastapi import FastAPI
import uvicorn


class api_fast:
    tall = []

    def get_fire_risk(predictions):
    
        tall = []
        for lines in predictions.firerisks:
            tall.append(lines.ttf)

        return tall

    def make_file(tall):
    
        with open("position.txt", "w") as fil:
            fil.write(str(tall))
        print(fil.closed)

    def open_fast_api(tall):

        app = FastAPI()

        @app.get("/")
        def root():
            return {"message": tall}
        

        
if __name__ == "__main__":

    tall = [1, 2, 3]

    api_fast.open_fast_api(tall)
    uvicorn.run(app, host="0.0.0.0", port=8000)
