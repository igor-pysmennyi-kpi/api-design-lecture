import psycopg2
from os import getenv

def connect():
    return psycopg2.connect(
        host=getenv('POSTGRES_HOST'),
        port=getenv('POSTGRES_PORT'),
        dbname=getenv('POSTGRES_DB'),
        user=getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'))