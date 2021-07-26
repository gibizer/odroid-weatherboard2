import json
import logging
import signal
import sys
from typing import Optional

import collector
import rest

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("bme280_main")

STORE: Optional[collector.Store] = None


class FakeDevice:
    @staticmethod
    def read():
        return 26.0, 50.0, 999.0


def main():
    LOG.info("Starting...")

    dev = collector.Device()
    store = collector.Store()
    store.load()
    c = collector.Collector(dev, store)
    c.start()

    def sigterm_handler(signum, frame):
        c.stop()

    signal.signal(signal.SIGTERM, sigterm_handler)

    rest.Wb2RestServer(store, port=55190).start()
    LOG.info("Exiting")


if __name__ == '__main__':
    main()
