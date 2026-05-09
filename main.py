from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

app = FastAPI(title="NEPSE Live API Proxy")

# Enable CORS so the API can be accessed from web apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NEPSE_API_URL = "https://nepselytics-6d61dea19f30.herokuapp.com/api/nepselytics/live-nepse"

@app.get("/")
def read_root():
    return {"message": "Welcome to the NEPSE Live API Proxy. Use /api/live to get data."}

@app.get("/api/live")
def get_live_data():
    try:
        response = requests.get(NEPSE_API_URL)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            return data.get("data", [])
        else:
            raise HTTPException(status_code=500, detail="External API returned an unsuccessful status.")
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from source API: {str(e)}")

if __name__ == "__main__":
    # This is for local testing
    uvicorn.run(app, host="0.0.0.0", port=8000)
