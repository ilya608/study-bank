from pydantic import BaseModel


class FeatureCollectorBankOutput(BaseModel):
    latitude: float
    longitude: float
