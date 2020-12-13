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
def get_dates():
    dates = {
        'today': str(datetime.date(datetime.now()) + timedelta(days=1)),
        'tomorrow': str(datetime.date(datetime.now()) + timedelta(days=2))
    }
    return dates
def get_vehicle_id(connection):
    with connection.cursor() as cursor:
        query = "select max(vehicle_id) from vehicles"
        cursor.execute(query)
        result = cursor.fetchall()
    print(result)
    return result[0]['max(vehicle_id)']
def create_car(connection, updatelocation, 
    vehicle_id, vehicle_model ,vehicle_make,vehicle_vin,vehicle_year,vehicle_license_plate_no,vehicle_available,vehicle_type_id,vehicle_type,vehicle_charge,vehicle_extra_charge,date):
    if vehicle_available == "yes":  vehicle_available = 1
    else:  vehicle_available = 0
    query = 'insert into vehicles values(vehicle_id,"vehicle_model","vehicle_make","vehicle_vin", "vehicle_year","vehicle_license_plate_no","vehicle_available","vehicle_type_id","updatelocation")'
    query2 = 'insert into vehicle_class values("vehicle_type_id","vehicle_type","vehicle_charge","vehicle_extra_charge")'
    print(query)
    print(query2)
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.execute(query2)
    connection.commit()
def get_car_info(connection, car):
    query = 'select * from vehicles where vehicle_id = {}'.format(car)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_car_class_info(connection,type_id):
    query = 'select * from vehicle_class where type_id = {}'.format(type_id)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


   



