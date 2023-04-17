from datetime import datetime
import time
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import logging


GLOBAL_CONFIG = {
    "model": {
        "serialized_model_path": "../model/flightdelay.pkl"
    },
    "service": {
        "log_path": "../logs/"
    }
}

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=GLOBAL_CONFIG['service']['log_path']
    )

class FlightDetails(BaseModel): 
    DepartureDateTime: str
    Origin: str
    Destination: str

with open(GLOBAL_CONFIG['model']['serialized_model_path'], 'rb') as f: 
    MODEL = pickle.load(f)


app = FastAPI()


@app.on_event("startup")
def startup_event():
    logging.info('Setup completed.')


@app.on_event("shutdown")
def shutdown_event():
    logging.info("Shutting down application")



def model_pred(departure_date_time, origin, destination, model=MODEL):
    """_summary_

    Args:
        departure_date_time (_type_): _description_
        origin (_type_): _description_
        destination (_type_): _description_

    Returns:
        _type_: _description_
    """

    try:
        departure_date_time_parsed = datetime.strptime(departure_date_time, '%d/%m/%Y %H:%M:%S')
    except ValueError as e:
        return 'Error parsing date/time - {}'.format(e)

    month = departure_date_time_parsed.month
    day = departure_date_time_parsed.day
    day_of_week = departure_date_time_parsed.isoweekday()
    hour = departure_date_time_parsed.hour

    origin = origin.upper()
    destination = destination.upper()

    input = [{'MONTH': month,
              'DAY_OF_MONTH': day,
              'DAY_OF_WEEK': day_of_week,
              'CRS_DEP_TIME': hour,
              'ORIGIN_ATL': 1 if origin == 'ATL' else 0,
              'ORIGIN_DTW': 1 if origin == 'DTW' else 0,
              'ORIGIN_JFK': 1 if origin == 'JFK' else 0,
              'ORIGIN_MSP': 1 if origin == 'MSP' else 0,
              'ORIGIN_SEA': 1 if origin == 'SEA' else 0,
              'DEST_ATL': 1 if destination == 'ATL' else 0,
              'DEST_DTW': 1 if destination == 'DTW' else 0,
              'DEST_JFK': 1 if destination == 'JFK' else 0,
              'DEST_MSP': 1 if destination == 'MSP' else 0,
              'DEST_SEA': 1 if destination == 'SEA' else 0 }]

    return model.predict_proba(pd.DataFrame(input))[0][0]

@app.get('/')
async def root():
    return {"hello": "world!"}


@app.post('/predict')
async def predict_delay(request: FlightDetails): 
    
    start = time.perf_counter()

    yhat = model_pred(departure_date_time= request.DepartureDateTime, origin=request.Origin, destination=request.Destination)

    end = time.perf_counter()

    latency = (end-start)*1000
    
    logging.debug({
        'request': request,
        'prediction':yhat,
        'latency': f'{latency:.3f} ms'})

    return {"Probability of arrival on time": yhat}




# alternative endpoint with query parameters

from enum import Enum

class Origin(str, Enum):
    JFK = "New York"
    SEA = "Seattle"
    ATL = "Atlanta"
    MSP = "Minneapolis"
    DTW = "Detroit"

class Destination(str, Enum):
    JFK = "New York"
    SEA = "Seattle"
    ATL = "Atlanta"
    MSP = "Minneapolis"
    DTW = "Detroit"


@app.post('/predictv2')
async def scoring_endpointv2(deptdatetime: str, origin: Origin, destination: Destination): 

    start = time.perf_counter()

    yhat = model_pred(departure_date_time=deptdatetime, origin=origin, destination=destination)

    end = time.perf_counter()

    latency = (end-start)*1000
    logging.debug({
        'request': {
        "DepartureDateTime": deptdatetime,
        "Origin": origin,
        "Destination": destination
        },
        'prediction':yhat,
        'latency': f'{latency:.3f} ms'})

    return {"Probability of arrival on time": yhat}
