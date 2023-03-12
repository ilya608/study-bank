from fastapi import FastAPI

from features_collector.feature_collector_manager import FeatureCollectorManager
from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from ml_models.predictor import Predictor
from utils.feature_transformer_for_ml import FeatureTransformerForMl

app = FastAPI()


@app.get("/abc")
async def root():
    return {"message": "Привет"}


@app.get("/predict-bank-quality")
def predict(lat: float, long: float):
    feature_collector_manager = FeatureCollectorManager()
    feature_transformer_for_ml = FeatureTransformerForMl()
    predictor = Predictor()

    feature_collector_bank_input = FeatureCollectorBankInput(latitude=lat, longitude=long)
    feature_collector_bank_output = feature_collector_manager.collect_features(feature_collector_bank_input)

    bank_input_for_ml = feature_transformer_for_ml.transform(feature_collector_bank_output)
    quality = predictor.predict(bank_input_for_ml)

    return {"quality": quality}
