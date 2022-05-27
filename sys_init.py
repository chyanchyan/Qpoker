from settings import *
import configparser
from sqlalchemy import create_engine


conf = configparser.ConfigParser()
conf.read('admin.ini')

db_param = {
    'type': DB_TYPE,
    'host': DB_HOST,
    'port': DB_PORT,
    'username': conf.get('db_params', 'username'),
    'psw': conf.get('db_params', 'psw'),
    'schema': DB_SCHEMA,
    'charset': DB_CHARSET,
}

url = '%(type)s+pymysql://%(username)s:%(psw)s@%(host)s/%(schema)s?charset=%(charset)s'
url = url % db_param


DB_ENGINE = create_engine(url=url)
