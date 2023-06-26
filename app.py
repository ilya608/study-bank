import logging
import pickle
import uuid

import psycopg2
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import Summary, Counter
from prometheus_fastapi_instrumentator import Instrumentator
from psycopg2 import pool
from pyinstrument import Profiler

from features_collector.feature_collector_manager import FeatureCollectorManager
from features_collector.input.feature_collector_bank_input import FeatureCollectorBankInput
from features_collector.postgres.avg_dao import AvgDao
from features_collector.postgres.menu_dao import MenuDao
from features_collector.postgres.regions_dao import RegionsDao
from logs.logs_dao import LogsDao
from ml.predictor import Predictor
from utils.feature_transformer_for_ml import FeatureTransformerForMl

REQUEST_TIME = Summary('general_response_time', 'Time spent processing request')
UPDATE_COUNT = Counter('request_per_seconds', 'Number of requests')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

Instrumentator().instrument(app).expose(app)

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,    # Минимальное количество соединений в пуле
    maxconn=10,   # Максимальное количество соединений в пуле
    host='rc1a-mxoodqvw58cvt97d.mdb.yandexcloud.net,rc1b-4ny0b4t0wrstwjaj.mdb.yandexcloud.net',
    port='6432',
    database='points',
    user='hse-ilya',
    password='12345678'
)
# psycopg2.connect("""
#         host=rc1a-mxoodqvw58cvt97d.mdb.yandexcloud.net,rc1b-4ny0b4t0wrstwjaj.mdb.yandexcloud.net
#         port=6432
#         sslmode=require
#         dbname=points
#         user=hse-ilya
#         password=12345678
#         target_session_attrs=read-write
#         sslrootcert=.postgresql/root.crt
#     """)

pg_connection = connection_pool.getconn()
avg_dao = AvgDao(pg_connection)
logs_dao = LogsDao(pg_connection)
menu_dao = MenuDao(pg_connection)
regions_dao = RegionsDao(pg_connection)

with open("ml/models/atm_best.pkl", "rb") as f:
    model = pickle.load(f)
predictor = Predictor(model)

feature_transformer_for_ml = FeatureTransformerForMl()

# Создание объекта логгера
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# Создание обработчика для записи логов в файл
file_handler = logging.FileHandler('logs/app.log')
file_handler.setLevel(logging.DEBUG)

# Создание форматтера для указания формата записи логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(reqId)s - %(message)s')

# Добавление форматтера к обработчику
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)
templates = Jinja2Templates(directory="static/templates")

print('okey')

logger.info('initialize logger', extra={'reqId': uuid.uuid4()})

id_to_bank_name = {'32': 'Райффайзен', '496': 'Россельхозбанк', '1022': 'АК Барс', '1942': 'Альфабанк', '3185': 'Газпромбанк', '5478': 'Уралсиб', '8083': 'Росбанк'}
bank_name_to_id = {value: float(key) for key, value in id_to_bank_name.items()}

def generate_request_id():
    return str(uuid.uuid4())


@app.get("/admin", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/debug", response_class=HTMLResponse)
def debug(request: Request):
    return templates.TemplateResponse("debug.html", {"request": request})


@app.get("/api-debug")
def predict(req_id: str):
    return logs_dao.select_logs(req_id)


@app.get("/config")
def config():
    return JSONResponse({'host': '51.250.21.70'})


@app.get("/menu-items")
def menu_items():
    items_json = menu_dao.get_menu_data()

    bank_names = []
    for id in items_json['atm_group']:
        bank_names.append(id_to_bank_name[id])
    items_json['atm_group'] = bank_names
    return JSONResponse(items_json)


@app.get("/menu-items")
def menu_items():
    items_json = menu_dao.get_menu_data()

    bank_names = []
    for id in items_json['atm_group']:
        bank_names.append(id_to_bank_name[id])
    items_json['atm_group'] = bank_names
    return JSONResponse(items_json)

@app.get("/predict-bank-quality-debug", response_class=HTMLResponse)
def predict_debug(lat: float, long: float, atm_group: str, city: str, region: str, state: str):
    profiler = Profiler()
    profiler.start()
    predict_inner(lat, long, atm_group, city, region, state)
    profiler.stop()
    return profiler.output_html()

@app.get("/predict-bank-quality")
def predict(lat: float, long: float, atm_group: str, city: str, region: str, state: str):
    content = predict_inner(lat, long, atm_group, city, region, state)

    return JSONResponse(content=content['content'], headers=content['headers'])

@REQUEST_TIME.time()
def predict_inner(lat: float, long: float, atm_group: str, city: str, region: str, state: str):
    UPDATE_COUNT.inc(1)

    atm_group = bank_name_to_id[atm_group]
    req_id = generate_request_id()
    logger.info('handle request: lat={}, long={}'.format(lat, long), extra={'reqId': req_id})
    feature_collector_manager = FeatureCollectorManager(connection_pool)

    feature_collector_bank_input = FeatureCollectorBankInput(latitude=lat, longitude=long, atm_group=atm_group,
                                                             city=city, region=region, state=state)
    feature_collector_bank_output = feature_collector_manager.collect_features(feature_collector_bank_input, logger,
                                                                               req_id)

    bank_row_dataframe = feature_transformer_for_ml.transform(feature_collector_bank_output, logger, req_id)
    quality = predictor.predict(bank_row_dataframe, logger, req_id)

    content = {"quality": str(round((quality[0] - (-0.145001)) / (0.218608 - (-0.145001)) * 100, 2)) + '%'}
    headers = {'Request-Id': req_id}

    feature_collector_manager.close()
    return {'content': content, 'headers': headers}
    # return JSONResponse(content=content, headers=headers)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# sudo docker-compose up --build -d app
