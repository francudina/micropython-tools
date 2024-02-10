import asyncio

from src.common import api
from src.common.device import Memory
from src.common.led import Led
from src.common.wifi import AioEspNow, WiFi

devices = {b"\xec\xda;\xbe\xd3\x08", b"\xec\xda;\xbf\x8f\xac"}

wlan = WiFi()
e = AioEspNow()

devices.remove(e.mac_address)
peers = list(devices)

e.register_peers(peers=peers)
print(f'mac: {e.mac_address}')

led = Led(pin=8, on_value=0, off_value=1)
led.blink(count=3, between=0.3)


async def send_info(esp_now, api_freq: float):
    url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m'
    Memory.enable_gc(enable=True)
    while True:
        # get data from api
        data: {} = api.get(url=url)
        # send it to peers
        val = data['current']['temperature_2m']
        print(f'sending value: {val}')

        # sent: {} = esp_now.send(message=val, peers=receivers)
        sent = {}
        for p in peers:
            try:
                sent[p] = await esp_now.get_esp_now().asend(p, str(val))
            except OSError as e:
                print(f'received OSError when sending message to peer (mac: {p}): {e}')

        if all([sent[p] for p in peers]):
            print(f'sent to: {sent}')
            led.blink(count=3, between=0.3)
        else:
            led.turn_off()
        # async sleep
        await asyncio.sleep(api_freq)


async def main(timeout: float, api_freq: float):
    asyncio.create_task(send_info(esp_now=e, api_freq=api_freq))
    while True:
        await asyncio.sleep(timeout)

asyncio.run(main(timeout=60, api_freq=10))
