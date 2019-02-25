import logging
import os
import yaml
import psycopg2
from datetime import datetime


def get_config(config_path='./config.yaml'):
    with open(config_path, encoding='utf-8') as f:
        config = yaml.load(f)
    return config


def folder_init(config):
    os.makedirs(config['folders']['log'], exist_ok=True)


def logger_init():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return now, formatter, logger


def get_credentials(credential_path='./credentials.local'):
    with open(credential_path, encoding='utf-8') as f:
        credentials = yaml.load(f)
    return credentials


def create_logger(logger, log_level, formatter, log_file=None):
    if log_file:
        log_handler = logging.FileHandler(filename=log_file, mode='w')
    else:
        log_handler = logging.StreamHandler()
    log_handler.setLevel(log_level)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)


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