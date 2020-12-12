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
        query = 'select vehicle_id, model, make, year, type, rent_charge from vehicles JOIN vehicle_class on ' \
                'vehicles.type_id=vehicle_class.type_id where office_id={} and availability=1'\
            .format(location)
    else:
        query = query = 'select vehicle_id, model, make, year, type, rent_charge from vehicles JOIN vehicle_class on ' \
                'vehicles.type_id=vehicle_class.type_id where office_id={} and availability=1 and type={}'\
            .format(location, type)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    for i in range(len(result)):
        result[i]['model'] = result[i]['model'].title()
        result[i]['make'] = result[i]['make'].title()
    return result


def get_location_info(connection, location):
    query = 'select * from offices where offices_id = {}'.format(location)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_car_info(connection, car):
    query = 'select * from vehicles where vehicle_id = {}'.format(car)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_car_class_info(connection,type_id):
    query = 'select rent_charge from vehicle_class where type_id = {}'.format(type_id)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_coupon_info(connection, coupon_id):
    if coupon_id == "":
        return [{'discount': 0, 'coupon_id': 0}]
    query = 'select discount, coupon_id from discounts where coupon_id = {}'.format(coupon_id)
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
        'today': str(datetime.date(datetime.now()) + timedelta(days=1)),
        'tomorrow': str(datetime.date(datetime.now()) + timedelta(days=2))
    }
    return dates


def insert_dummy_data(connection):
    query = "insert into discounts values (11, 35, STR_TO_DATE('01/01/2021', '%d/%m/%y'),STR_TO_DATE('01/05/2021', '%d/%m/%y'))"

    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()


def generate_cust_id(connection):
    query = 'select max(cust_id) from customer'
    with connection.cursor as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def generate_rental_id(connection):
    with connection.cursor() as cursor:
        query = "select max(rental_id) from rentals"
        cursor.execute(query)
        result = cursor.fetchall()

    print(result)
    return result[0]['max(rental_id)']


def get_invoice_id(connection):
    with connection.cursor() as cursor:
        query = "select max(invoice_id) from invoice"
        cursor.execute(query)
        result = cursor.fetchall()

    print(result)
    return result[0]['max(invoice_id)']


def create_rental(connection, info):
    query = "insert into rentals values({},STR_TO_DATE('{}','%Y-%m-%d'),STR_TO_DATE('{}','%Y-%m-%d'),null, null,{},{},{},{},{},{},{}, 0)".format(
        info['rental_id'], info['pickup_date'], info['dropoff_date'], 150, info['invoice_id'], info['coupon_id'],
        info['vehicle_id'], info['cust_id'], info['pickup_office'], info['dropoff_office'])
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()


def create_invoice(connection, invoice_id, end_date, total_amount):
    start_date = str(datetime.date(datetime.now()))
    print(start_date)
    print(end_date)
    query = "insert into invoice values({},STR_TO_DATE('{}','%Y-%m-%d'), STR_TO_DATE('{}','%Y-%m-%d'), {})".format(
        invoice_id, start_date, end_date, total_amount)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()


def calculate_total(start_date, end_date, coupon, rent_charge):
    date_format = "%Y-%m-%d"
    end_date = datetime.strptime(end_date, date_format)
    start_date = datetime.strptime(start_date, date_format)
    delta = end_date - start_date
    days = delta.days
    return (100.00-float(coupon))*float(days)*float(rent_charge)*0.01
