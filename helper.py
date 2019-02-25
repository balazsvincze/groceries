import logging
import os
import json
from datetime import datetime
import yaml


def get_config(config_path='./config.yaml'):
    with open(config_path, encoding='utf-8') as f:
        config = yaml.load(f)
    return config


def folder_init(config):
    os.makedirs(config['folders']['log'], exist_ok=True)
    os.makedirs(config['folders']['screenshots'], exist_ok=True)


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


def save_screenshot(driver, config, counter, file_prefix):
    if config['with_screenshot']:
        file_path = f'{config["folders"]["screenshots"]}/{file_prefix}{counter:04d}.png'
        driver.save_screenshot(file_path)
        return file_path
    else:
        return ''
