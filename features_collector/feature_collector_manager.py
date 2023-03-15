from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput
from features_collector.postgres.PostgresDao import PostgresDao


class FeatureCollectorManager:
    def __init__(self):
        self.postgres_dao = PostgresDao()

    def collect_features(self, feature_collector_bank_input: FeatureCollectorBankInput) -> FeatureCollectorBankOutput:
        lat = feature_collector_bank_input.latitude
        long = feature_collector_bank_input.longitude

        # todo тут должна быть вся логика которая будет собирать фичи из бд, делать http запросы(если нужно итд)
        # ответ она должна свой положить в FeatureCollectorBankOutput

        return FeatureCollectorBankOutput(latitude=lat, longitude=long)
