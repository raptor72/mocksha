#!/usr/bin/python3

# -*- coding: utf-8 -*-

import json
import logging
from optparse import OptionParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from filehandler import get_strict_responses
from reghandler import get_regexp_responses

OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}


def many_people_handler(req):
    try:
        body = req["body"]
        if type(body) == dict:
            logging.info(f"request_json: {body}")
            for fish in strict_responses:
                logging.info(f"fish: {fish}")
                if body in fish and body != fish[-1]:
                    return fish[-1]
                else:
                    continue
            for fish in regexp_responses:
                matched = fish[0].match(str(body))
                logging.info(f"matched: {matched}")
                if matched:
                    return fish[-1]
                else:
                    continue
            return {"problem 1": "could not find response for current request"}
    except json.decoder.JSONDecodeError:
        logging.error("Could not decode request as json")
        return {"Problem 2": "JSONDecodeError"}


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "many_people": many_people_handler
    }
    store = None

    def do_POST(self):
        response, code = {}, OK
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
            logging.info(f"request is: {request}")
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info(f"self.path is: {self.path}, data_string is: {data_string}")
            if path in self.router:
                try:
                    response = self.router[path]({"body": request, "headers": self.headers})
                except Exception as e:
                    logging.exception(f"Unexpected error: {e}")
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND
        logging.info(f"code is: {code}")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        # logging.info(f"r is: {r}")
        self.wfile.write(bytes(str(json.dumps(r)).encode()))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8089)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    strict_responses = get_strict_responses()
    regexp_responses = get_regexp_responses()
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    logging.info(f"strict_responses is: {strict_responses}")
    logging.info(f"regexp_responses is: {regexp_responses}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
