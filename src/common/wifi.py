import espnow
import network
import ubinascii

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


class EspNow:
    _esp_now: espnow.ESPNow
    mac_address: bytes

    def __init__(self):
        # network config
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # mac config
        self.mac_address = wlan.config('mac')
        # esp now config
        self._esp_now = espnow.ESPNow()
        self._esp_now.active(True)

    def register_peers(self, peers: [bytes]):
        for p in peers:
            self._esp_now.add_peer(p)

    def remove_peers(self, peers: [bytes]):
        for p in peers:
            self._esp_now.del_peer(p)

    def send(self, message, peers: [bytes] = None, sync: bool = True) -> {}:
        sent = {}
        for p in peers:
            try:
                sent[p] = self._esp_now.send(p, message, sync)
            except OSError as e:
                print(f'received OSError when sending message to peer (mac: {p}): {e}')
        return sent

    def receive(self, wait_timeout_ms: int) -> {}:
        received = {}
        start = ticks_ms()
        while ticks_diff(ticks_ms(), start) < wait_timeout_ms:
            mac, message = self._esp_now.recv()
            # msg == None then it was timeout in recv()
            if message:
                received.setdefault(mac, []).append(message)
        return received
