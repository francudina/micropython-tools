from utime import sleep

from src.common.led import Led
from src.common.wifi import EspNow


devices = {b"\xec\xda;\xbe\xd3\x08", b"\xec\xda;\xbf\x8f\xac"}

e = EspNow()

devices.remove(e.mac_address)
peers = list(devices)

e.register_peers(peers=peers)
print(f'receiver: {e.mac_address}')

led = Led(pin=8, on_value=0, off_value=1)
while True:
    received: {} = e.receive(wait_timeout_ms=300)
    if len(received) != 0:
        print(f'received: {received}')
        led.blink(count=1, between=0.3)
    sleep(0.01)
