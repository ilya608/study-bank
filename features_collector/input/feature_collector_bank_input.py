from pydantic import BaseModel


class FeatureCollectorBankInput(BaseModel):
    latitude: float
    longitude: float
