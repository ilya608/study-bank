import csv
import random

from features_collector.output.feature_collector_bank_output import FeatureCollectorBankOutput


def extract_distance_features_names():
    features = []
    for attr_name in dir(FeatureCollectorBankOutput):
        if attr_name.startswith('distance_to_'):
            feature_name = attr_name[len('distance_to_'):]
            features.append(feature_name)
    return features


# Определяем количество записей
num_records = 200

features = extract_distance_features_names()

# Создаем список со случайными значениями широты, долготы и типом здания
data = [(round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6),
         random.choice(features)) for _ in range(num_records)]

# Открываем файл для записи
with open("points.csv", "w", newline="") as csvfile:
    # Создаем объект writer для записи в CSV файл
    writer = csv.writer(csvfile, delimiter=",")

    # Записываем заголовок
    writer.writerow(["latitude", "longitude", "building_type"])

    # Записываем данные
    for record in data:
        writer.writerow(record)
