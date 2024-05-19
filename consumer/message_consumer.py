import json
import logging
import os

from confluent_kafka import Consumer


class MessageConsumer(Consumer):
    def __init__(self, topic: str, group_id: str):
        self.broker_host = os.getenv("KAFKA_BROKER_URL")
        self.broker_port = os.getenv("KAFKA_BROKER_PORT")
        self.topic = topic
        super().__init__(
            {
                'bootstrap.servers': f"{self.broker_host}:{self.broker_port}",
                'group.id': group_id,
                'auto.offset.reset': 'earliest'
            }
        )
        self.subscribe([self.topic])
        logging.info("Consumer has been initiated and subscribe to topic '%s'", self.topic)

    def get_message(self):
        message = self.poll(1.0)
        if message is None:
            return None
        if error := message.error():
            logging.error("error: %s", error)
            return None
        return message.value().decode('utf-8')

    def get_data(self):
        if message := self.get_message():
            return json.loads(message)
        return None
