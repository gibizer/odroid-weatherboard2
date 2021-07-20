import json
import logging
import signal
import sys

import collector
import ws

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("bme280_main")

STORE = None


def sigterm_handler(signum, frame):
    # lets save the data if we are being killed
    if STORE:
        with open("data.save", "w") as f:
            json.dump(STORE.read(), f)
            LOG.info("Data saved to disk before terminating")
    sys.exit(0)


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

    ws.start(store, port=55190)
    LOG.info("Exiting")


if __name__ == '__main__':
    main()
