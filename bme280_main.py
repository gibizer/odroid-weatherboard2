import json
import logging
import signal
import sys
from typing import Optional

import collector
import ws
import rest

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("bme280_main")

STORE: Optional[collector.Store] = None


def sigterm_handler(signum, frame):
    # lets save the data if we are being killed
    if STORE:
        with open("data.save", "w") as f:
            json.dump(STORE.read(), f)
            LOG.info("Data saved to disk before terminating")
    sys.exit(0)


class FakeDevice:
    @staticmethod
    def read():
        return 26.0, 50.0, 999.0


def main():
    LOG.info("Starting...")

    # load saved data from disk
    try:
        with open("data.save", "r") as f:
            data = json.load(f)            
    except Exception:
        # no saved data
        data = []

    dev = collector.Device()
    store = collector.Store(data)
    global STORE
    STORE = store
    c = collector.Collector(dev, store)
    c.start()

    signal.signal(signal.SIGTERM, sigterm_handler)

    rest.Wb2RestServer(store, port=55190).start()
    LOG.info("Exiting")


if __name__ == '__main__':
    main()
