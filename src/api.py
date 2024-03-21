from fastapi import FastAPI, HTTPException
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/write_position/")
async def write_position(latitude: float, longitude: float):
    try:
        # Logging latitude and longitude
        logger.info(f"Received latitude: {latitude}, longitude: {longitude}")

        # Printing latitude and longitude
        print(f"Received latitude: {latitude}, longitude: {longitude}")

        with open("position.txt", "w") as f:
            f.write(f"Latitude: {latitude}, Longitude: {longitude}")
        return {"message": "Position has been written to position.txt"}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
