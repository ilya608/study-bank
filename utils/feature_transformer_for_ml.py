from typing import List

from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput
from ml_models.input.bank_input_for_ml import BankInputForML


class FeatureTransformerForMl:
    def __init__(self):
        self.todo = 123

    def transform(self, bank_with_features: FeatureCollectorBankOutput) -> BankInputForML:
        return BankInputForML(bank_with_features.latitude, bank_with_features.longitude)
