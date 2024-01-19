import random
import machine

from utime import sleep

from src.common.led import Led
from src.common.pub_sub import PubSubClient
from src.common.wifi import WiFi


def publish_readings():
    publish_topic = 'readings'

    wlan = WiFi(retry_count=10)
    if not wlan.is_connected():
        sleep(2)
        print('(Publisher): Failed to connect to Wi-Fi. Retrying...')
        machine.reset()

    led = Led(15)
    led.turn_off()

    client = PubSubClient()

    while True:
        try:
            reading = random.uniform(0, 10)
            print(f'> generated: {reading}')

            led.blink(count=5, between=0.3)
            client.publish(topic=publish_topic, message=str(reading))

            sleep(10)
        except OSError as e:
            client = PubSubClient()
