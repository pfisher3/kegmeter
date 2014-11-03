import logging
import threading
import time

from DB import DB

class TapStatus(object):
    def __init__(self, tap_id):
        self.tap_id = tap_id
        self.pulses = 0
        self.clear()

    def update(self, pulses):
        self.pulses += pulses
        self.last_update = time.time()

    def is_done(self):
        return (self.last_update is not None and self.last_update < time.time() - 5)

    def clear(self):
        if self.pulses > 0:
            DB.update_amount_poured(self.tap_id, self.pulses)

        self.pulses = 0
        self.last_update = None


class KegmeterStatus(object):
    def __init__(self):
        self.tap_update_event = threading.Event()
        self.temp_update_event = threading.Event()
        self.interrupt_event = threading.Event()

        self.tap_statuses = dict()
        self.temp_statuses = dict()

    def interrupt(self, signal, frame):
        logging.error("Got keyboard interrupt, exiting")
        self.interrupt_event.set()

    def add_tap(self, tap_id):
        self.tap_statuses[tap_id] = TapStatus(tap_id)

    def update_tap(self, tap_id, pulses):
        self.tap_update_event.set()
        self.tap_statuses[tap_id].update(pulses)

    def cleanup_taps(self):
        for tap in self.tap_statuses.values():
            if tap.is_done():
                self.tap_update_event.set()
                tap.clear()

    def get_active_tap(self):
        for tap in self.tap_statuses.values():
            if tap.last_update is not None:
                return tap

    def update_temp(self, temp_id, temp):
        self.temp_update_event.set()
        self.temp_statuses[temp_id] = temp
