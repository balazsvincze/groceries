import helper
import logging
import pydb
from configparser import ConfigParser


def init(config):
    helper.folder_init(config)
    now, formatter, logger = helper.logger_init()
    helper.create_logger(logger, logging.INFO, formatter, f'{config["folders"]["log"]}/{now}_info_log.txt')
    helper.create_logger(logger, logging.ERROR, formatter, f'{config["folders"]["log"]}/{now}_error_log.txt')
    helper.create_logger(logger, logging.INFO, formatter)
 

def main():
    config = helper.get_config()
    init(config)
    credentials = helper.get_credentials('./credentials.local')

    # DB Example
    conn = pydb.connect(config, credentials)
    cur = conn.cursor()
    cur.execute('select current_timestamp')
    print(cur.fetchall())
    pydb.connect_teardown(conn)


if __name__ == '__main__':
    main()