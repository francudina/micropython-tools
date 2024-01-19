import network

from src.common import secrets
from utime import sleep, ticks_ms, ticks_diff


# defaults
WIFI_RETRY = 10     # count
CONNECTION_WAIT = 1


class WiFi:
    _wlan: network.WLAN

    def __init__(self, retry_count: int = WIFI_RETRY):
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)

        start = ticks_ms()
        self._wlan.connect(secrets.SSID, secrets.PASSWORD)

        while not self._wlan.isconnected() and retry_count > 0:
            print(f'> ({retry_count}) waiting for connection...')
            sleep(CONNECTION_WAIT)
            retry_count -= 1

        delta = ticks_diff(ticks_ms(), start)
        if not self._wlan.isconnected():
            print('(e) network connection failed')
        else:
            print(f'(i) connected after {delta} [ms]')
            print('(i) IP: ' + self._wlan.ifconfig()[0])

    def is_connected(self) -> bool:
        return self._wlan.isconnected()

    def reconnect(self, retry_count: int = WIFI_RETRY):
        self.__init__(retry_count)
