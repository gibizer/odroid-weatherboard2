import collections
import datetime
import json
import logging
import time
import threading

import BME280


LOG = logging.getLogger('collector')


class Device:
    def __init__(self):
        self.bme = BME280.BME280(
            '/dev/i2c-1',
            # forced mode would be better
            p_mode=0x03,
            # 2x oversample
            h_samp=0x02, p_samp=0x02, t_samp=0x02
        )
        # put it in sleep
        self.bme.set_power_mode(0x00)

    def read(self):
        # wake up
        self.bme.set_power_mode(0x03)
        time.sleep(0.1)

        press = self.bme.read_pressure()

        if str(press) == "67638.19849463052":
            LOG.info("Device is in reset, restart it.")
            self.bme.set_power_mode(0x00)
            time.sleep(0.1)
            self.bme.set_power_mode(0x03)

        temp = self.bme.read_temperature()
        hum = self.bme.read_humidity()
        press = self.bme.read_pressure()

        # put it in sleep
        self.bme.set_power_mode(0x00)
        return temp, hum, press


class Store:
    def __init__(self, data, nr_of_data=2*24*60*2):
        self.lock = threading.RLock()
        self.deque = collections.deque(
            data, maxlen=nr_of_data)
        LOG.info(
            f"Data store initialized with {len(self.deque)} data points")

    def store(self, data):
        with self.lock:
            self.deque.append(data)

    def read(self):
        with self.lock:
            return list(self.deque)


class Collector:
    def __init__(self, device: Device, store: Store):
        self.dev = device
        self.store = store
        self.thread = threading.Thread(target=self._run)
        self.last_saved = datetime.datetime.now()

    def start(self):
        self.thread.start()
        LOG.info("Collector started")

    def _run(self):
        i = 0
        while True:
            time.sleep(30)
            data = self.dev.read()
            data =  (str(datetime.datetime.now()), *data)            
            self.store.store(data)
            i += 1
            # log temp to syslog every 5 minutes
            if i == 10:
                i = 0
                LOG.info(
                    f"temp={data[1]}, hum={data[2]}, press={data[3]}")
            # save data to disk daily
            if datetime.datetime.now() - self.last_saved > datetime.timedelta(days=1):
                with open("data.save", "w") as f:
                    json.dump(self.store.read(), f)
                    LOG.info("Saved data to disk")
                self.last_saved = datetime.datetime.now()

