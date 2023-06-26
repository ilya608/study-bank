from prometheus_client import Summary

from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput
from features_collector.postgres.avg_dao import AvgDao
from features_collector.postgres.points_dao import PointsDao
from features_collector.postgres.regions_dao import RegionsDao

REQUEST_TIME = Summary('collect_features_response_time', 'Time spent processing request')


class FeatureCollectorManager:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

        self.conn1 = self.connection_pool.getconn()
        self.conn2 = self.connection_pool.getconn()
        self.conn3 = self.connection_pool.getconn()

        self.points_dao = PointsDao(self.conn1)
        self.avg_dao = AvgDao(self.conn2)
        self.regions_dao = RegionsDao(self.conn3)

    def close(self):
        self.connection_pool.putconn(self.conn1)
        self.connection_pool.putconn(self.conn1)
        self.connection_pool.putconn(self.conn1)

    @REQUEST_TIME.time()
    def collect_features(self,
                         feature_collector_bank_input: FeatureCollectorBankInput,
                         logger,
                         req_id) -> FeatureCollectorBankOutput:
        logger.info('start feature collect', extra={'reqId': req_id})

        lat = feature_collector_bank_input.latitude
        long = feature_collector_bank_input.longitude

        nearest_by_type = self.points_dao.get_nearest_points(lat, long, logger, req_id)

        logger.info('nearest_by_type points {}'.format(len(nearest_by_type)), extra={'reqId': req_id})

        feature_collector_bank_output = FeatureCollectorBankOutput()

        self.calculate_distance_features(nearest_by_type, feature_collector_bank_output, logger, req_id)
        self.calculate_avg_features(feature_collector_bank_input, feature_collector_bank_output, logger, req_id)
        self.calculate_cnt200m_features(feature_collector_bank_input, feature_collector_bank_output, logger, req_id)
        self.calculate_regions_features(feature_collector_bank_input, feature_collector_bank_output, logger, req_id)
        self.calculate_query_features(feature_collector_bank_input, feature_collector_bank_output)

        return feature_collector_bank_output

    def calculate_query_features(self,
                                 feature_collector_bank_input: FeatureCollectorBankInput,
                                 feature_collector_bank_output: FeatureCollectorBankOutput):
        feature_collector_bank_output.states = feature_collector_bank_input.state
        feature_collector_bank_output.cities = feature_collector_bank_input.city
        feature_collector_bank_output.regions = feature_collector_bank_input.region
        feature_collector_bank_output.atm_group = feature_collector_bank_input.atm_group

    def calculate_distance_features(self, nearest_by_type, feature_collector_bank_output: FeatureCollectorBankOutput,
                                    logger, req_id):
        for point in nearest_by_type:
            type = point['building_type']
            distance = point['min_distance']

            feature_name = 'distance_to_' + type
            if hasattr(feature_collector_bank_output, feature_name):
                setattr(feature_collector_bank_output, feature_name, distance)
            else:
                logger.error("failed parse points", extra={'reqId': req_id})

    def calculate_cnt200m_features(self,
                                   feature_collector_bank_input: FeatureCollectorBankInput,
                                   feature_collector_bank_output: FeatureCollectorBankOutput,
                                   logger,
                                   req_id):
        data = self.points_dao.get_cnt200m_points(feature_collector_bank_input.latitude,
                                                  feature_collector_bank_input.longitude,
                                                  logger,
                                                  req_id)
        feature_collector_bank_output.cnt_banks_200m = data.get('bank', 0)
        feature_collector_bank_output.cnt_atm_200m = sum(
            data[i] for i in data.keys() if len(i) >= 4 and i[-4:] == 'bank' or i[-3:] == 'atm')
        feature_collector_bank_output.cnt_apart_200m = data.get('apart', 0)

        return data

    def calculate_avg_features(self,
                               feature_collector_bank_input: FeatureCollectorBankInput,
                               feature_collector_bank_output: FeatureCollectorBankOutput,
                               logger,
                               req_id):
        logger.info('calculate avg_features', extra={'reqId': req_id})

        avg_features = self.avg_dao.get_avg_features_data(feature_collector_bank_input.atm_group,
                                                          feature_collector_bank_input.city,
                                                          feature_collector_bank_input.region,
                                                          feature_collector_bank_input.state,
                                                          logger,
                                                          req_id)
        feature_collector_bank_output.avgA = avg_features['atm_group']
        feature_collector_bank_output.avgC = avg_features['cities']
        feature_collector_bank_output.avgR = avg_features['regions']
        feature_collector_bank_output.avgS = avg_features['states']

    def calculate_regions_features(self,
                                   feature_collector_bank_input: FeatureCollectorBankInput,
                                   feature_collector_bank_output: FeatureCollectorBankOutput,
                                   logger,
                                   req_id):
        logger.info('calculate regions_features', extra={'reqId': req_id})

        regions_features = self.regions_dao.get_regions_data(feature_collector_bank_input.region,
                                                             logger,
                                                             req_id)
        feature_collector_bank_output.population = regions_features['population']
        feature_collector_bank_output.salary = regions_features['salary']
        feature_collector_bank_output.population_density = regions_features['population_density']
        feature_collector_bank_output.happy_index = regions_features['happy_index']
