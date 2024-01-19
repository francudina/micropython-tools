try:
    # some esp chip doesn't support this library, but esp8266 does
    import ssd1306
except:
    pass
import framebuf

from micropython import const
from utime import sleep, sleep_ms
from machine import Pin, I2C, SPI


# defaults
# - Esp8266Display
WIDTH = 128
HEIGHT = 64

SDA_PIN = 12
SCL_PIN = 14

EMPTY_SCREEN_COLOR = 0
TEXT_COLOR = 1


class Esp8266Display:
    """
    Docs: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
    """
    _width: int
    _height: int
    _display: ssd1306.SSD1306_I2C

    def __init__(self, width: int = WIDTH, height: int = HEIGHT):
        self._width = width
        self._height = height
        i2c = I2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        self._display = ssd1306.SSD1306_I2C(width, height, i2c)
        self.reset()

    def reset(self):
        self._display.fill(EMPTY_SCREEN_COLOR)
        self._display.show()

    def on(self):
        self._display.poweron()

    def off(self):
        self._display.poweroff()

    def message(self,
                message: str,
                row: int = 0,
                reset_before: bool = True,
                reset_after: bool = True,
                duration_s: float = None):
        if reset_before:
            self.reset()

        self._display.text(message, 0, row, TEXT_COLOR)
        self._display.show()

        if duration_s:
            sleep(duration_s)

        if not duration_s and reset_after:
            self.reset()


_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)


class Matrix8x8:
    def __init__(self, cs_pin: int):
        number_of_matrices = 1
        cs = Pin(cs_pin)
        self.spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * number_of_matrices)
        self.num = number_of_matrices
        fb = framebuf.FrameBuffer(self.buffer, 8 * number_of_matrices, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        self.fill = fb.fill             # (col)
        self.pixel = fb.pixel           # (x, y[, c])
        self.hline = fb.hline           # (x, y, w, col)
        self.vline = fb.vline           # (x, y, h, col)
        self.line = fb.line             # (x1, y1, x2, y2, col)
        self.rect = fb.rect             # (x, y, w, h, col)
        self.fill_rect = fb.fill_rect   # (x, y, w, h, col)
        self.text = fb.text             # (string, x, y, col=1)
        self.scroll = fb.scroll         # (dx, dy)
        self.blit = fb.blit             # (fbuf, x, y[, key])
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)

    def scrolling_message(self, message: str, invert_color: bool = False):
        fill_color = 1 if invert_color else 0
        # clear display
        self.fill(fill_color)
        self.show()
        # calculate number of columns of the message
        column = (len(message) * 8)
        for x in range(32, -column, -1):
            # clear display
            self.fill(fill_color)
            # write the scrolling text in to frame buffer
            self.text(message, x, 1, abs(fill_color-1))
            # show
            self.show()
            # set the scrolling speed (50ms)
            sleep(0.05)
