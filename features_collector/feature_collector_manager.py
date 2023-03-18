from logging import getLogger

from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput

from features_collector.postgres.points_dao import PointsDao


class FeatureCollectorManager:
    def __init__(self, points_dao: PointsDao):
        self.points_dao = points_dao

    def collect_features(self, feature_collector_bank_input: FeatureCollectorBankInput) -> FeatureCollectorBankOutput:
        lat = feature_collector_bank_input.latitude
        long = feature_collector_bank_input.longitude
        nearest_by_type = self.points_dao.get_nearest_points(lat, long)

        feature_collector_bank_output = FeatureCollectorBankOutput()
        self.parse_points(nearest_by_type, feature_collector_bank_output)
        # todo тут должна быть вся логика которая будет собирать фичи из бд, делать http запросы(если нужно итд)

        return feature_collector_bank_output


    def parse_points(self, nearest_by_type, feature_collector_bank_output: FeatureCollectorBankOutput):
        for point in nearest_by_type:
            type = point['building_type']
            distance = point['min_distance']

            feature_name = 'distance_to_' + type
            if hasattr(feature_collector_bank_output, feature_name):
                setattr(feature_collector_bank_output, feature_name, distance)
            else:
                raise Exception("fixme") # todo сделать тут логирование вместо exception. это ок, если пришла незнакомая фича
