import pandas as pd
from prometheus_client import Summary

from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput

renaming_rules = {'distance_to_bank_sberbank': 'distance_to_bank_Сбербанк',
                  'distance_to_bank_vtb': 'distance_to_bank_ВТБ',
                  'distance_to_bank_alfa_bank': 'distance_to_bank_Альфа-Банк',
                  'distance_to_bank_rosbank': 'distance_to_bank_Росбанк',
                  'distance_to_atm_sberbank': 'distance_to_atm_Сбербанк',
                  'distance_to_atm_vtb': 'distance_to_atm_ВТБ',
                  'distance_to_atm_alfa_bank': 'distance_to_atm_Альфа-Банк',
                  'distance_to_atm_rosbank': 'distance_to_atm_Росбанк'
                  }

REQUEST_TIME = Summary('ml_model_response_time', 'Time spent processing request')


def rename_russian_features(bank):
    for fr, to in renaming_rules.items():
        val = bank[fr]
        bank[to] = val
        del bank[fr]
    return bank


class FeatureTransformerForMl:
    def __init__(self):
        self.todo = 123

    @REQUEST_TIME.time()
    def transform(bank: FeatureCollectorBankOutput) -> pd.DataFrame:
        json = vars(bank)
        json = rename_russian_features(json)
        series = pd.Series(json)
        return series.to_frame().T
