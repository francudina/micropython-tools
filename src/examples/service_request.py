from sys import exit

from src.common import api
from src.common.led import Led
from src.common.wifi import WiFi
from src.common.input import Button
from utime import sleep

def api_status():
    led = Led(pin=2)
    wlan = WiFi()

    if not wlan.is_connected():
        led.blink(count=3, between=0.3)
        exit(1)

    led.turn_on()

    status: {} = api.get(url='http://localhost:8080/actuator/health')
    if not status:
        led.blink(count=5, between=0.3)
        exit(1)

    print(f'info: {status}')
    led.blink(count=4, between=0.5)

    return status


def button_press():
    button = Button(pin=23, callback=lambda x: print("button pressed"))
    wlan = WiFi()

    if not wlan.is_connected():
        exit(1)

    while True:
        print("falling asleep..")
        sleep(5)
