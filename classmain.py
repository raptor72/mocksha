#!/usr/bin/python3

# -*- coding: utf-8 -*-


import json
import logging
from optparse import OptionParser
from http.server import BaseHTTPRequestHandler, HTTPServer

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


def method_handler(req):
    logging.info(f"req is: {req}")
    logging.info(f"req headers is: {req['headers']}")
    return req["body"]

class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def do_POST(self):
        response, code = {}, OK
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            logging.info(f"self.headers is: {self.headers}")
            request = json.loads(data_string)
            logging.info(f"request is: {request}")
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info(f"self.path is:  {self.path}, data_string is: {data_string}")
            if path in self.router:
                try:
                    logging.info(f"self.headers is: {self.headers}")
                    response = self.router[path]({"body": request, "headers": self.headers})
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
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
        # context.update(r)
        logging.info(f"r is: {r}")
        self.wfile.write(bytes(str(json.dumps(r)).encode()))
        return r


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8089)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()