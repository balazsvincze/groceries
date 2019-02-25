import psycopg2
import logging


def connect(config, credentials):
    conn = None
    try:
        logging.info('Connecting to the PostgreSQL database...')
        return psycopg2.connect(host=config['database']['host'], 
                                dbname=config['database']['db_name'], 
                                user=credentials['user'], 
                                password=credentials['password'])
 
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)


def connect_teardown(conn):
    if conn is not None:
        conn.close()
        logging.info('Database connection closed.')