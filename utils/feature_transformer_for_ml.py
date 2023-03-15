from typing import List

from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput
from ml.input.bank_input_for_ml import BankInputForML

import pandas as pd

renaming_rules = {'distance_to_bank_sberbank': 'distance_to_bank_Сбербанк',
                  'distance_to_bank_vtb': 'distance_to_bank_ВТБ',
                  'distance_to_bank_alfa_bank': 'distance_to_bank_Альфа-Банк',
                  'distance_to_bank_rosbank': 'distance_to_bank_Росбанк',
                  'distance_to_atm_sberbank': 'distance_to_atm_Сбербанк',
                  'distance_to_atm_vtb': 'distance_to_atm_ВТБ',
                  'distance_to_atm_alfa_bank': 'distance_to_atm_Альфа-Банк',
                  'distance_to_atm_rosbank': 'distance_to_atm_Росбанк'
                  }


def rename_russian_features(bank):
    for fr, to in renaming_rules.items():
        val = bank[fr]
        bank[to] = val
        del bank[fr]
    return bank


class FeatureTransformerForMl:
    def __init__(self):
        self.todo = 123

    @staticmethod
    def transform(bank_with_features: FeatureCollectorBankOutput) -> pd.DataFrame:
        bank_input_for_ml = BankInputForML(atm_group=123)  # todo переложить тут bank_with_features сюда

        json = vars(bank_input_for_ml)
        json = rename_russian_features(json)
        series = pd.Series(json)
        return series.to_frame().T
