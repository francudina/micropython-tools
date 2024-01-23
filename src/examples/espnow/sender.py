import ubinascii

from utime import sleep

from src.common.led import Led
from src.common.wifi import EspNow


devices = {b"H'\xe2^E\x8c", b"H'\xe2^E\x1e"}

e = EspNow()

print(f'mac: {e.mac_address}')

devices.remove(e.mac_address)
peers = list(devices)

e.register_peers(peers=peers)

led = Led(pin=15)
while True:
    sent: {} = e.send(message=b'hi there :)', peers=peers, sync=True)
    if all([sent[p] for p in peers]):
        print(f'sent to: {sent}')
        led.blink(count=3, between=0.3)
    else:
        led.turn_off()
    sleep(3)
