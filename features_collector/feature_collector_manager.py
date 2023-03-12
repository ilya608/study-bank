from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput


class FeatureCollectorManager:
    def __init__(self):
        self.todo = 123

    def collect_features(self, feature_collector_bank_input: FeatureCollectorBankInput) -> FeatureCollectorBankOutput:
        lat = feature_collector_bank_input.latitude
        long = feature_collector_bank_input.longitude

        # todo тут должна быть вся логика которая будет собирать фичи

        return FeatureCollectorBankOutput(latitude=lat, longitude=long)
