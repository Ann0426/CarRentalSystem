import pymysql
import json
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

## Switch to relative path during deployment
CONFIG = './config.txt'


def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print('Check Path')


def get_configs():
    key = load_key()
    f = Fernet(key)
    try:
        with open(CONFIG, 'rb') as infile:
            config = json.loads(infile.read())
        for each in config.keys():
            config[each] = f.decrypt(config[each].encode()).decode()
        return config
    except FileNotFoundError:
        print('Check Path')


def create_connection():
    configs = get_configs()
    connection = pymysql.connect(host=configs['host'],
                                 user=configs['user'],
                                 password=configs['password'],
                                 db=configs['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_office_locations(connection):
    with connection.cursor() as cursor:
        query = 'select * from offices'
        cursor.execute(query)
        result = cursor.fetchall()
    for i in range(len(result)):
        result[i]['offices_id'] = int(result[i]['offices_id'])
    return result


def get_available_cars(connection, location, type):
    if type == 'all':
        query = 'select vehicle_id, model, make, year from vehicles where office_id={} and availability=1'.format(location, type)
    else:
        query = 'select vehicle_id, model, make from vehicles where office_id={} and availability=1'.format(location)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_query_response(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_dates():
    dates = {
        'today': str(datetime.date(datetime.now())),
        'tomorrow': str(datetime.date(datetime.now()) + timedelta(days=1))
    }
    return dates