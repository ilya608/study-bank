from logging import getLogger

from prometheus_client import Summary

from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput

from features_collector.postgres.points_dao import PointsDao

REQUEST_TIME = Summary('collect_features_response_time', 'Time spent processing request')


class FeatureCollectorManager:
    def __init__(self, points_dao: PointsDao):
        self.points_dao = points_dao

    @REQUEST_TIME.time()
    def collect_features(self, feature_collector_bank_input: FeatureCollectorBankInput, logger,
                         req_id) -> FeatureCollectorBankOutput:
        logger.info('start feature collect', extra={'reqId': req_id})

        lat = feature_collector_bank_input.latitude
        long = feature_collector_bank_input.longitude
        nearest_by_type = self.points_dao.get_nearest_points(lat, long)

        logger.info('nearest_by_type points {}'.format(len(nearest_by_type)), extra={'reqId': req_id})

        feature_collector_bank_output = FeatureCollectorBankOutput()
        self.parse_points(nearest_by_type, feature_collector_bank_output, logger, req_id)
        # todo тут должна быть вся логика которая будет собирать фичи из бд, делать http запросы(если нужно итд)

        return feature_collector_bank_output

    def parse_points(self, nearest_by_type, feature_collector_bank_output: FeatureCollectorBankOutput, logger, req_id):
        for point in nearest_by_type:
            type = point['building_type']
            distance = point['min_distance']

            feature_name = 'distance_to_' + type
            if hasattr(feature_collector_bank_output, feature_name):
                setattr(feature_collector_bank_output, feature_name, distance)
            else:
                logger.error("failed parse points", extra={'reqId': req_id})
