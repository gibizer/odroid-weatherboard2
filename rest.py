import json
import logging

import bottle


LOG = logging.getLogger("rest")


class Wb2RestServer:
    def __init__(self, store, port):
        self.app = bottle.Bottle()
        self.store = store
        self.port = port
        self._setup_routes()

    def start(self):
        bottle.run(
            self.app, host='0.0.0.0', port=self.port)

    def _setup_routes(self):
        @self.app.get('/measurements')
        def get_measurements():
            """Return the list of measurements"""
            bottle.response.headers['Content-Type'] = 'application/json'
            bottle.response.headers['Cache-Control'] = 'no-cache'
            return json.dumps(self.store.read()).encode()


