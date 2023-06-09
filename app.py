import pickle

import uvicorn
from fastapi import FastAPI
from prometheus_client import Summary, Counter
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import create_engine

from features_collector.feature_collector_manager import FeatureCollectorManager
from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.postgres.points_dao import PointsDao
from features_collector.postgres.postgres_connection import get_pg_connection
from ml.predictor import Predictor
from utils.feature_transformer_for_ml import FeatureTransformerForMl

REQUEST_TIME = Summary('general_response_time', 'Time spent processing request')
UPDATE_COUNT = Counter('request_per_seconds', 'Number of requests')

app = FastAPI()

Instrumentator().instrument(app).expose(app)

pg_connection = get_pg_connection()
points_dao = PointsDao(pg_connection)

with open("ml/models/atm_best.pkl", "rb") as f:
    model = pickle.load(f)
feature_collector_manager = FeatureCollectorManager(points_dao)
predictor = Predictor(model)


@REQUEST_TIME.time()
@app.get("/predict-bank-quality")
def predict(lat: float, long: float):
    UPDATE_COUNT.inc(1)
    feature_collector_bank_input = FeatureCollectorBankInput(latitude=lat, longitude=long)
    feature_collector_bank_output = feature_collector_manager.collect_features(feature_collector_bank_input)

    bank_row_dataframe = FeatureTransformerForMl.transform(feature_collector_bank_output)
    quality = predictor.predict(bank_row_dataframe)

    return {"quality": quality[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# sudo docker-compose up --build -d app
