import os

from consumer.consumer import MessageConsumer
from consumer.email_generator import EmailGenerator


class Starter:
    def __init__(self):
        self.consumer = MessageConsumer(
            topic=os.getenv("TOKEN"),
            group_id=os.getenv("GROUP_ID")
        )

    def start(self):
        while True:
            data = self.consumer.get_data()
            if (
                data
                and (notification_template := data.get("notification_template", None))
                and (extra_parameters := data.get("extra_parameters", None))
                and (to_email := data.get("to_email", None))
                and (custom_data := data.get("custom_data", None))
            ):
                EmailGenerator(
                    notification_template=notification_template,
                    extra_parameters=extra_parameters,
                    to_email=to_email,
                    custom_data=custom_data
                ).send()
