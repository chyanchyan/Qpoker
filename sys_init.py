from settings import *
import configparser
from sqlalchemy import create_engine


admin_ini_path = r'C:\Users\Q\Desktop\db_admin.ini'

conf = configparser.ConfigParser()
conf.read(admin_ini_path)

db_param = {
    'type': DB_TYPE,
    'host': DB_HOST,
    'port': DB_PORT,
    'username': conf.get('db_admin', 'username'),
    'password': conf.get('db_admin', 'password'),
    'schema': DB_SCHEMA,
    'charset': DB_CHARSET,
}

url = '%(type)s+pymysql://%(username)s:%(password)s@%(host)s/%(schema)s?charset=%(charset)s'
url = url % db_param


DB_ENGINE = create_engine(url=url)
