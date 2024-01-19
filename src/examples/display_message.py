import json

from src.common.display import Esp8266Display, Matrix8x8
from src.common.input import MembraneKeypad3x1
from src.common.sensors import DHT22
from src.examples import service_request


def api_message():
    display = Esp8266Display()
    display.on()

    status: {} = service_request.api_status()

    display.message(message=json.dumps(status), duration_s=3.0)
    display.off()


def keypad_message():
    display = Esp8266Display()
    display.on()

    keypad = MembraneKeypad3x1()

    display.message(f'use semaphore', duration_s=1.0)
    display.message('in: <empty>', reset_after=False)

    readings: [] = keypad.wait_input(timeout_ms=5000, expected_input_count=3)
    if len(readings) != 0:
        display.message(f'in: {"".join(readings)}', duration_s=1.5)

    display.message('bye :)', duration_s=2.0)
    display.off()


def temperature_message():
    display = Esp8266Display()
    display.on()

    sensor = DHT22(pin=5)

    display.message(f'Current reading:', row=0, reset_before=True, duration_s=1.0)
    display.message(f'temp: {sensor.temperature()}C', row=16, reset_before=False, duration_s=1.0)
    display.message(f'hum: {sensor.humidity()}%', row=32, reset_before=False, duration_s=1.0)

    display.off()


def temperature_console_message():
    sensor = DHT22(pin=5)

    print(f'Current reading:')
    print(f'temp: {sensor.temperature()}C')
    print(f'hum: {sensor.humidity()}%')


def matrix_character():
    display = Matrix8x8(cs_pin=15)
    display.brightness(5)

    display.text('a', 0, 0, 1)
    display.show()


def matrix_stars():
    display = Matrix8x8(cs_pin=15)
    display.brightness(5)

    display.text('ž', 0, 0, 1)
    display.show()


def matrix_scrolling_message():
    display = Matrix8x8(cs_pin=15)
    display.brightness(5)

    display.scrolling_message(message='Hi there :)')


def matrix_scrolling_message_color_inversion():
    display = Matrix8x8(cs_pin=15)
    display.brightness(5)

    display.scrolling_message(message='Hi there :)', invert_color=True)
