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

