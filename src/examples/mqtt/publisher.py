import random
import machine

from utime import sleep

from src.common.device import Memory
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


def publish_dht_reading():
    # topics
    # - status
    device_online_topic = 'device_online'
    device_active_topic = 'device_active'
    device_fault_topic = 'device_fault'

    # - readings
    current_temperature_topic = 'current_temperature'

    wlan = WiFi(retry_count=10)
    if not wlan.is_connected():
        sleep(2)
        print('(Publisher): Failed to connect to Wi-Fi. Retrying after machine reset...')
        machine.reset()

    Memory.enable_gc(True)

    client = PubSubClient()
    print(f'MQTT client id: {client.get_client_id()}')

    # device is online
    client.publish(topic=device_online_topic, message=str(True))

    led = Led(pin=8, on_value=0, off_value=1)
    sensor = DHT22(pin=4)

    led.blink(count=3, between=0.3)

    # device is active
    client.publish(topic=device_active_topic, message=str(True))

    error_count = 0
    while True:
        try:
            reading = sensor.temperature()
            print(f'temperature: {reading}')

            client.publish(topic=current_temperature_topic, message=str(reading))
            led.blink(count=5, between=0.3)

            sleep(10)
        except OSError as e:
            print(f'Device OSError: {e}')
            client = PubSubClient()
            client.publish(topic=device_fault_topic, message=str(True))
        except Exception as e:
            print(f'Device Exception: {e}')
            client.publish(topic=device_fault_topic, message=str(True))
            error_count += 1
            if error_count > 3:
                machine.reset()
