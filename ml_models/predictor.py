import random

from ml_models.input.bank_input_for_ml import BankInputForML


class Predictor:
    def __init__(self):
        self.todo = 123

    def predict(self, bank_entry: BankInputForML) -> float:
        # todo ML здесь
        return random.random()