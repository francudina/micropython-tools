import asyncio

from src.common.device import Memory
from src.common.led import Led
from src.common.wifi import AioEspNow

devices = {b"\xec\xda;\xbe\xd3\x08", b"\xec\xda;\xbf\x8f\xac"}

e = AioEspNow()

devices.remove(e.mac_address)
peers = list(devices)

e.register_peers(peers=peers)
print(f'mac: {e.mac_address}')

led = Led(pin=8, on_value=0, off_value=1)
led.blink(count=3, between=0.3)


async def blink():
    led.blink(count=1, between=0.25)


async def get_info(esp_now):
    Memory.enable_gc(enable=True)
    while True:
        # check messages
        received: {} = await esp_now.receive()
        if not received:
            continue
        print("received:", received)
        await blink()


asyncio.run(get_info(esp_now=e))
