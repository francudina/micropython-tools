from machine import Pin
from utime import sleep, ticks_ms, ticks_diff


# defaults
# - pin shouldn't be one of the TX pins (e.g. TXD0)
ROW_1_PIN = 14
ROW_2_PIN = 12
ROW_3_PIN = 13
# - column pin (only one present)
COLUMN_1_PIN = 15

ROW_1_COLOR = 'R'
ROW_2_COLOR = 'Y'
ROW_3_COLOR = 'G'

TIME_BETWEEN_READINGS = 0.17


class MembraneKeypad3x1:
    _r1: Pin
    _r2: Pin
    _r3: Pin
    _c1: Pin
    _color: {}

    def __init__(self,
                 p1: int = ROW_1_PIN,
                 p2: int = ROW_2_PIN,
                 p3: int = ROW_3_PIN,
                 c1: int = COLUMN_1_PIN):
        self._r1 = Pin(p1, Pin.OUT)
        self._r2 = Pin(p2, Pin.OUT)
        self._r3 = Pin(p3, Pin.OUT)
        self._c1 = Pin(c1, Pin.IN)
        self._color = {
            ROW_1_COLOR: self._r1,
            ROW_2_COLOR: self._r2,
            ROW_3_COLOR: self._r3
        }

    def _read_row(self, color: str) -> str | None:
        if color not in self._color.keys():
            return None
        row: Pin = self._color[color]
        row.value(1)
        clicked = None
        if self._c1.value() == 1:
            clicked = color
        row.value(0)
        return clicked

    def wait_input(self, timeout_ms: float = 2000, expected_input_count: int = 1) -> [str]:
        inputs: [str] = []
        t_start = ticks_ms()

        while len(inputs) < expected_input_count:
            t_elapsed = ticks_diff(ticks_ms(), t_start)
            if 0 < timeout_ms <= t_elapsed:
                break

            for color in self._color.keys():
                if self._read_row(color):
                    inputs.append(color)

            sleep(TIME_BETWEEN_READINGS)

        return inputs[:expected_input_count]


class Button:
    _button: Pin

    def __init__(self, pin: int, callback):
        self._button = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self._button.irq(callback, trigger=Pin.IRQ_FALLING)
