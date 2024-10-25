import json
import logging
import time
import struct
import zlib

import bottle


LOG = logging.getLogger("rest")


# Gzip handling copied from
# https://stackoverflow.com/questions/47240972/httpie-can-not-decode-my-bottle-api-gzipped-respond
def write_gzip_header():
    header = b'\037\213'      # magic header
    header += b'\010'         # compression method
    header += b'\0'
    header += struct.pack("<L", int(time.time()))
    header += b'\002'
    header += b'\377'
    return header


def write_gzip_trailer(crc, size):
    footer = struct.pack("<q", crc)
    footer += struct.pack("<L", size & 0xFFFFFFFF)
    return footer


def gzip_body(data):
    yield write_gzip_header()
    crc = zlib.crc32(b"")
    size = 0
    zobj = zlib.compressobj(
        6, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
    size += len(data)
    crc = zlib.crc32(data, crc)
    yield zobj.compress(data)
    yield zobj.flush()
    yield write_gzip_trailer(crc, size)


class Wb2RestServer:
    def __init__(self, store, port):
        self.app = bottle.Bottle()
        self.store = store
        self.port = port
        self._setup_routes()

    def start(self):
        bottle.run(
            self.app,
            server='cheroot',
            host='0.0.0.0', port=self.port)

    def _setup_routes(self):
        @self.app.get('/measurements')
        def get_measurements():
            """Return the list of measurements"""
            bottle.response.headers['Content-Type'] = 'application/json'
            bottle.response.headers['Cache-Control'] = 'no-cache'

            # allow calling this API from anywhere
            bottle.response.set_header('Access-Control-Allow-Origin', '*')
            bottle.response.add_header(
                'Access-Control-Allow-Methods', 'GET, OPTIONS')

            data = json.dumps(self.store.read()).encode('utf-8')
            # save bandwidth, would be nicer to do this in a real web server
            if 'gzip' in bottle.request.headers.get('Accept-Encoding', ''):
                bottle.response.headers['Content-Encoding'] = 'gzip'
                data = gzip_body(data)
            else:
                bottle.response.headers['Content-Encoding'] = 'identity'

            return data
