import yadisk
import json
from yadisk import exceptions

# Take token
with open(r'D:\1. Other\1. Work\1. Programming\# keys\Yandex Drive\yandex_token.json') as f:
    token = json.load(f).get('access_token')

# Authorisation and send request
y = yadisk.YaDisk(token=token)

try:
    y.upload(r'.\data\NBA_data.csv', '/538/NBA_data.csv')
except exceptions.PathExistsError:
    y.remove('/538/NBA_data.csv', permanently=True)
    y.upload(r'.\data\NBA_data.csv', '/538/NBA_data.csv')

