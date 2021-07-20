import logging
import json

from simple_websocket_server import WebSocketServer, WebSocket


LOG = logging.getLogger("websocket")

class Exporter(WebSocket):
    store = None

    def handle(self):
        # for any message we return all the data
        self.send_message(json.dumps(self.store.read()))

    def connected(self):
        #LOG.info(f"connection from {self.address}")
        pass

    def handle_close(self):
        #LOG.info(f"connection closed: {self.address}")
        pass


def start(store, port):
    Exporter.store = store
    server = WebSocketServer('', port, Exporter)
    LOG.info('Websocket started')
    server.serve_forever()

