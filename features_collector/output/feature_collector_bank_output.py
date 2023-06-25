from dataclasses import dataclass


@dataclass
class FeatureCollectorBankOutput:
    atm_group: float = 0.0

    distance_to_fast_food: float = 1000.0
    distance_to_clothes: float = 1000.0
    distance_to_vending_parking: float = 1000.0
    distance_to_cafe: float = 1000.0
    distance_to_pharmacy: float = 1000.0
    distance_to_atm: float = 1000.0
    distance_to_cinema: float = 1000.0
    distance_to_shoe_shop: float = 1000.0
    distance_to_bank: float = 1000.0
    distance_to_supermarket: float = 1000.0
    distance_to_restaurant: float = 1000.0
    distance_to_mobile_phone_shop: float = 1000.0
    distance_to_convenience: float = 1000.0
    distance_to_vending_any: float = 1000.0
    distance_to_bank_sberbank: float = 1000.0
    distance_to_bank_vtb: float = 1000.0
    distance_to_bank_alfa_bank: float = 1000.0
    distance_to_bank_rosbank: float = 1000.0
    distance_to_atm_sberbank: float = 1000.0
    distance_to_atm_vtb: float = 1000.0
    distance_to_atm_alfa_bank: float = 1000.0
    distance_to_atm_rosbank: float = 1000.0
    distance_to_retail: float = 1000.0
    distance_to_residential: float = 1000.0
    distance_to_office: float = 1000.0
    distance_to_commercial: float = 1000.0
    distance_to_detached: float = 1000.0
    distance_to_train_station: float = 1000.0
    distance_to_apartments: float = 1000.0
    distance_to_house: float = 1000.0
    distance_to_railway_halt: float = 1000.0
    distance_to_tram_stop: float = 1000.0
    distance_to_bus_stop: float = 1000.0
    distance_to_railway_station: float = 1000.0
    distance_to_airport: float = 1000.0
    distance_to_parking: float = 1000.0
    distance_to_parking_underground: float = 1000.0
    # конец фичей которые есть

    cnt_apart_200m: float = 0.0
    cnt_banks_200m: float = 0.0
    cnt_atm_200m: float = 0.0
    cities: str = ''
    regions: str = ''
    states: str = ''
    population: float = 0.0
    salary: float = 0.0
    population_density: float = 0.0
    happy_index: float = 0.0
    capital: float = 0.0
    avgC: float = 0.0
    avgR: float = 0.0
    avgS: float = 0.0
    avgA: float = 0.0
