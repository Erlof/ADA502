from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    with open("position.txt", "r") as fil:
        text = ''
        for lines in fil:
            text = text + lines + '\n'
        # print(text)
        return {"message": text}
