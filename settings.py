import os
from datetime import datetime
from pathlib import Path

# Токен Тиньков Инвестиций
TOKEN = os.getenv('TINKOFF_TOKEN')
# Идентификатор портфеля в Тиньков инвестициях, его можно получить так:
# tinvest.UserApi(client).accounts_get().parse_json().payload
BROKER_ACCOUNT_ID = os.getenv('TINKOFF_BROKER_ACCOUNT')
# Дата, от которой будут получены пополнения портфеля
BROKER_ACCOUNT_STARTED_AT = datetime.strptime(os.getenv('TINKOFF_ACCOUNT_STARTED'),
                                              '%d.%m.%Y')
# Местоположение таблицы, куда складывать данные
CSV_NAME = 'stats.csv'
CSV_DIR = Path('./data/')