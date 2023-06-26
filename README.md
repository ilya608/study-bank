# Сервис по расчету популярности расположения банкомата
### *Study bank project for predict bank place quality*

Сервис предлагает пользователю оценить предлагаемое расположение банкомата.
Пользователь вводит в географических координатах Широту, Долготу будущего местоположения банкомата, а также название банка-владельца, город, регион и федеральный округ.

Результатом станет рейтинг предложенного местоположения, где $0%$ - очень плохое место, а $100%$ - лучшее место для банкомата.

*Примечание: вкладки Метрики и Дебаг являются техническими и отвечают за логирование и мониторинг ошибок сервиса*

```bash
├── Dockerfile
├── README.md
├── app.py
├── common
│   └── point.py
├── database_initializer
│   ├── CsvForTest.py
│   ├── avg_table
│   │   ├── avg_table_initializer.py
│   │   └── regions_table_initializer.py
│   ├── database_initializer_for_test.py
│   └── points_initializer.py
├── docker-compose.yml
├── features_collector
│   ├── feature_collector_manager.py
│   ├── input
│   │   └── feature_collector_bank_input.py
│   ├── output
│   │   └── feature_collector_bank_output.py
│   └── postgres
│       ├── avg_dao.py
│       ├── menu_dao.py
│       ├── points_dao.py
│       ├── postgres_connection.py
│       └── regions_dao.py
├── grafana
│   └── dashboards
│       └── settings.json
├── logs
│   ├── Dockerfile
│   ├── dump_to_postgres.py
│   ├── logs_dao.py
│   └── requirements1.txt
├── ml
│   ├── input
│   │   └── bank_input_for_ml.py
│   ├── models
│   │   └── atm_best.pkl
│   └── predictor.py
├── nginx
│   └── nginx.conf
├── prometheus.yml
├── requirements.txt
├── static
│   ├── styles.css
│   └── templates
│       ├── admin.html
│       ├── debug.html
│       └── index.html
├── test
│   └── load.py
└── utils
    └── feature_transformer_for_ml.py
```

### Варианты запуска
1. Должно подниматься такой командой на порту 8000:
`docker-compose up --build`

Запрос чтобы потестить:
http://0.0.0.0:8000/predict-bank-quality?lat=123&long=34

2. По ссылке:
http://51.250.21.70:8000/ 
