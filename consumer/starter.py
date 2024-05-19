import os

from message_consumer import MessageConsumer
from email_generator import EmailGenerator


class Starter:
    def __init__(self, start: bool = True):
        self.consumer = MessageConsumer(
            topic=os.getenv("TOPIC"),
            group_id=os.getenv("GROUP_ID")
        )

        if start:
            self.start()

    def start(self):
        while True:
            data = self.consumer.get_data()
            if (
                data
                and (template := data.get("template"))
                and (username := data.get("username"))
                and (client_email := data.get("client_email"))
                and (address := data.get("address"))
            ):
                EmailGenerator(
                    template=template,
                    username=username,
                    client_email=client_email,
                    address=address
                ).send()
