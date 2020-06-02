#!/usr/bin/python3

import os
import json
import logging


def load_sample(files_path):
    with open(files_path, 'rb') as conf:
        template = json.load(conf, encoding='utf8')
    return template


def get_strict_responses(logdir="stricts"):
    if not os.path.exists(logdir):
        logging.info("Log directory does not exists")
        return
    if not os.listdir(logdir):
        logging.info("Directory is empty")
        return
    strict_responses = []
    for response_file in os.listdir(logdir):
        logging.info(f'response_file is: {response_file}')
        try:
            strict = load_sample(os.path.join(logdir, response_file))
            strict_responses.append(strict)
        except json.decoder.JSONDecodeError:
            logging.error(f'Could not load file: {response_file}')
            continue
    return strict_responses


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    print(get_strict_responses())