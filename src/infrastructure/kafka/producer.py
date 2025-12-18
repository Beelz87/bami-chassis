from confluent_kafka import Producer
from src.infrastructure.config.settings import settings
from src.infrastructure.logging.logger import get_logger

logger = get_logger("kafka")

class KafkaProducer:
    def __init__(self):
        self.producer_config = {
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'client.id': settings.service_name,
        }
        self._producer = None

    def get_producer(self):
        if self._producer is None:
            self._producer = Producer(self.producer_config)
        return self._producer

    def send_message(self, topic: str, value: str, key: str = None):
        try:
            producer = self.get_producer()
            producer.produce(topic=topic, key=key, value=value,
                           callback=self._delivery_callback)
            producer.poll(0)  # Trigger callbacks
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    def _delivery_callback(self, err, msg):
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(f"Message delivered to {msg.topic()}")

    def flush(self):
        if self._producer:
            self._producer.flush()

kafka_producer = KafkaProducer()
