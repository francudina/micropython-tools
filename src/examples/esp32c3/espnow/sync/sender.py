from utime import sleep

from src.common.led import Led
from src.common.wifi import EspNow


devices = {b"\xec\xda;\xbe\xd3\x08", b"\xec\xda;\xbf\x8f\xac"}

e = EspNow()

print(f'mac: {e.mac_address}')

devices.remove(e.mac_address)
peers = list(devices)

e.register_peers(peers=peers)

led = Led(pin=8, on_value=0, off_value=1)
while True:
    sent: {} = e.send(message=b'hi there :)', peers=peers, sync=True)
    if all([sent[p] for p in peers]):
        print(f'sent to: {sent}')
        led.blink(count=3, between=0.3)
    else:
        led.turn_off()
    sleep(3)
