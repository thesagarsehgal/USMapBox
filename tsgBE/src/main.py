from fastapi import FastAPI
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from .controllers import boundaries_controller, data_controller


app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boundaries_controller.router)
app.include_router(data_controller.router)


@app.get("/")
def read_root():
    return {"message": "Geospatial API Service"}


# state_boundaries_file_path = Path(__file__).parent / "data/gz_2010_us_040_00_20m.json"
# county_boundaries_file_path = Path(__file__).parent / "data/gz_2010_us_050_00_20m.json"


# @app.get("/api/v1/states")
# def get_state_boundaries():
#     with open(state_boundaries_file_path, "r") as file:
#         data = json.load(file)
#     return data

# @app.get("/api/v1/counties")
# def get_counties_boundaries():
#     with open(county_boundaries_file_path, "r") as file:
#         data = json.load(file)
#     return data