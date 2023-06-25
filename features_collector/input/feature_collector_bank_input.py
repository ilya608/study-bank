from pydantic import BaseModel


class FeatureCollectorBankInput(BaseModel):
    latitude: float
    longitude: float
    atm_group: float
    city: str
    region: str
    state: str


