#!/usr/bin/python3

import re
import os
import json
import logging


def load_regexp(files_path):
    with open(files_path, 'r') as regfile:
        res = []
        for line in regfile:
            res.append(line)
        pattern = re.compile(res[0].strip())
    return [pattern, json.loads(res[1])]


def get_regexp_responses(logdir="regexps"):
    if not os.path.exists(logdir):
        logging.info("Log directory does not exists")
        return
    if not os.listdir(logdir):
        logging.info("Directory is empty")
        return
    regexp_responses = []
    for response_file in os.listdir(logdir):
        logging.info(f'response_file is: {response_file}')
        try:
            regexp = load_regexp(os.path.join(logdir, response_file))
            regexp_responses.append(regexp)
        except:
            logging.error(f'Could not load file: {response_file}')
            continue
    return regexp_responses

