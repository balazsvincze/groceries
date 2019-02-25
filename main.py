import helper
import logging
import tesco


def init(config):
    helper.folder_init(config)
    now, formatter, logger = helper.logger_init()
    # helper.create_logger(logger, logging.INFO, formatter, f'{config["folders"]["log"]}/{now}_info_log.txt')
    # helper.create_logger(logger, logging.ERROR, formatter, f'{config["folders"]["log"]}/{now}_error_log.txt')
    helper.create_logger(logger, logging.INFO, formatter)
 

def main():
    config = helper.get_config()
    init(config)

    logging.info('Tesco Scraper has starterd')
    tesco.scrape_tesco()

if __name__ == '__main__':
    main()