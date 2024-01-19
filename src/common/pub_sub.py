import gc
import esp
import machine
import ubinascii

from src.common.umqttsimple import MQTTClient

esp.osdebug(None)
gc.collect()

# defaults
MQTT_BROKER = 'broker.hivemq.com'


class PubSubClient:
    _client: MQTTClient
    _client_id: str

    _broker: str

    def __init__(self, mqtt_broker: str = MQTT_BROKER):
        # config
        self._broker = mqtt_broker
        # client
        self._client_id = ubinascii.hexlify(machine.unique_id())
        self._client = MQTTClient(self._client_id, mqtt_broker)
        self._client.connect()
        print(f'Connected to {mqtt_broker} MQTT broker')

    def publish(self, topic: str, message: str):
        self._client.publish(topic, message)

    def subscribe(self, topic: str, callback):
        self._client.set_callback(callback)
        self._client.subscribe(topic)
        print(f'Subscribed to {topic} topic')

    def check_message(self) -> str:
        # nonblocking check
        return self._client.check_msg()
