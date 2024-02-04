from utime import sleep
from machine import Pin


# defaults
LED_ON = 1
LED_OFF = 0

LED_BLINK = 2       # count
LED_SLEEP = 0.5     # [s]


class Led:
    _led: Pin
    on_value: int
    off_value: int

    def __init__(self, pin: int, on_value: int = LED_ON, off_value: int = LED_OFF):
        self._led = Pin(pin, Pin.OUT)
        self.on_value = on_value
        self.off_value = off_value

    def turn_on(self, keep_on: float = None):
        self._led.value(self.on_value)
        if keep_on:
            sleep(keep_on)
            self.turn_off()

    def turn_off(self, keep_off: float = None):
        self._led.value(self.off_value)
        if keep_off:
            sleep(keep_off)
            self.turn_on()

    def invert(self):
        self._led.value(not self._led.value())

    def blink(self, count: int = LED_BLINK, between: float = LED_SLEEP):
        while count > 0:
            self.turn_off()
            sleep(between)
            self.turn_on()
            sleep(between)
            count -= 1
        self.turn_off()
