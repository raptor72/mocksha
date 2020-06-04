#!/usr/bin/python3

import re
import os
import json
import logging
from filehandler import load_sample

def load_regexp(files_path):
    with open(files_path, 'r') as regfile:
        res = []
        for line in regfile:
#            print(line)
            res.append(line)
#        regexp = regfile.split('\n')[0]
#        response = json.load(regfile.split('\n')[1], encoding='utf8')
#    return res[0].strip(), res[1]
#    return res[0].strip(), json.load(res[1], encoding='utf8')
#    return res[0].strip(), json.loads(res[1])
        pattern = re.compile(res[0].strip())
        # print(pattern)
        # print(type(pattern))
    return [pattern, json.loads(res[1])]

# a, b = load_sample('regexps/reg1')
# print(a)
# print(b)


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


print(get_regexp_responses())


#["{\S+: {\S+: \S+}, '\w+': '\w{1,6}', '\S{1,4}': \['\w+', '\w+', '\w+'\]}", {"regResp0": "value regexp response 0"}]
sample = [load_sample('stricts/sample4.json')]
print(sample)
#pattern = re.compile('{\w+: {\w+:\w+}, \w+: \w+, \w+: [\w+, \w+, \w+]}')
#pattern = re.compile("{'.*'}")
#pattern = re.compile("{\S+: {\S+: \S+}, '\w+': '\w{1,6}', '\S{1,4}': \[['\w{1,3}']{1,3}.*}")
pattern = re.compile("{\S+: {\S+: \S+}, '\w+': '\w{1,6}', '\S{1,4}': \['\w+', '\w+', '\w+'\]}")
print(pattern)

for i in sample:
    print(i)
    matched = pattern.match(str(i))
    print('matched: ', matched)
    print(type(matched))
