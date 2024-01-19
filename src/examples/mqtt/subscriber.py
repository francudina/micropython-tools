import machine

from utime import sleep

from src.common.led import Led
from src.common.pub_sub import PubSubClient
from src.common.wifi import WiFi


def subscribe_on_readings():
    sensor_readings = []
    subscribe_topic = 'readings'

    def callback(topic, message):
        message = message.decode("utf-8")
        topic = topic.decode("utf-8")
        print(f'(m) {topic}: {message}')
        if topic == subscribe_topic:
            sensor_readings.append(message)
            print(f'> total readings: {len(sensor_readings)}')
            led.turn_on(keep_on=1.5)

    wlan = WiFi(retry_count=10)
    if not wlan.is_connected():
        sleep(2)
        print('(Subscriber): Failed to connect to Wi-Fi. Retrying...')
        machine.reset()

    led = Led(15)
    led.turn_off()

    client = PubSubClient()
    client.subscribe(topic=subscribe_topic, callback=callback)

    while True:
        try:
            client.check_message()
            sleep(1)
        except OSError as e:
            client = PubSubClient()
