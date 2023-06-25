import pandas as pd


class Predictor:
    def __init__(self, model):
        self.model = model

    def predict(self, bank_entry: pd.DataFrame, logger, req_id) -> float:
        return self.model.predict(bank_entry)
