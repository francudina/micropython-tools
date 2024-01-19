import dht

from machine import Pin


class DHTSensor:
    _sensor: dht.DHT11 | dht.DHT22

    def __init__(self, sensor: dht.DHT11 | dht.DHT22):
        self._sensor = sensor

    def _measure(self):
        self._sensor.measure()

    def temperature(self) -> float:
        self._measure()
        return self._sensor.temperature()

    def humidity(self) -> float:
        self._measure()
        return self._sensor.humidity()


class DHT11(DHTSensor):
    def __init__(self, pin: int):
        super().__init__(dht.DHT11(Pin(pin)))


class DHT22(DHTSensor):
    def __init__(self, pin: int):
        super().__init__(dht.DHT22(Pin(pin)))
