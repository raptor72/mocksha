import sys
import json
import socket
import logging
import datetime
from filehandler import get_last_log

REQUEST_PARAMS = {
    'Host': 'Host',
    'User-Agent': 'User-Agent',
    'Content-Length': 'Content-Length',
    'Content-Type': 'Content-Type'
}


def read_all(sock, maxbuff, TIMEOUT=5):
    data = b''
    sock.settimeout(TIMEOUT)
    while True:
        buf = sock.recv(maxbuff)
        data += buf
        if not buf or b'\r\n\r\n' in data:
            break
    return data


def parse_request(request):
    headers = {}
    parsed = request.split('\r\n\r\n')[0].split(' ')
    method = parsed[0]
    for i in request.split('\r\n'):
        try:
            headers.update({REQUEST_PARAMS[i.split(':')[0]]: i.split(':')[1].strip()})
        except:
            continue
    return method, headers


def generate_response(request):
    method, headers = parse_request(request)
    if method not in ['POST']:
        return ('HTTP/1.1 405 Method not allowed\r\n', 405, None)
    if headers == {}:
        return ('HTTP/1.1 422 Can not parse headers format\r\n', 422, None)
    if not 'json' in headers['Content-Type']:
        return ('HTTP/1.1 400 Unsupported Content-Type\r\n', 400, None)
    request_json = request.split('\r\n\r\n')[1]
    return ('HTTP/1.1 200 OK\r\n', 200, request_json)


def make_mock_response(response_prase, code, request_json):
    if code != 200:
        logging.error(f'{response_prase}')
        return bytes(str({"problem 3": "could not find response"}).encode())
    strict_responses = get_last_log()
    logging.info(f'strict_responses is: {strict_responses}')
    try:
        d = json.loads(request_json)
        for fish in strict_responses:
            logging.info(f'request_json: {request_json}')
            logging.info(f'fish: {fish}')

            if d in fish:
                return bytes(str(fish[-1]).encode())
            else:
                continue
        return bytes(str({"problem 1": "could not find response"}).encode())
    except json.decoder.JSONDecodeError:
         logging.error('Could not find strict response')
         return bytes(str({"problem 2": "JSONDecodeError:"}).encode())

def generate_headers(response_prase):
    server = 'Server: python ' + sys.version.split('[')[0].strip() + ' ' +  sys.version.split('[')[1].strip().replace(']', '') + '\r\n'
    date = 'Date: ' + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + '\r\n'
    connection = 'Connection: close\r\n\r\n'
    headers = ''.join([response_prase, server, date, connection])
    return headers


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8088))
    server_socket.listen()
    while True:
        client_socket, addr = server_socket.accept()
        request = read_all(client_socket, maxbuff=2048)
        logging.info(f'request is: {request}')
        logging.info(f'address is: {addr}')
        if len(request.strip()) == 0:
            client_socket.close()
            continue
        if request:
            response_prase, code, request_json = generate_response(request.decode('utf-8'))
            headers = generate_headers(response_prase)
            json_response = make_mock_response(response_prase, code, request_json)
            client_socket.sendall(headers.encode() + json_response)
        client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    run()