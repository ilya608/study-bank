import random

from ml_models.input.bank_input_for_ml import BankInputForML


class MlManager:
    def __init__(self):
        self.todo = 123

    def predict(self, bank_with_features: Feature) -> float:
        # todo ML здесь
        return random.random()