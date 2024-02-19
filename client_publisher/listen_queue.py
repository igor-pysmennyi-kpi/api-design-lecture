import time
from random import randint
from typing import TYPE_CHECKING

import pika

if TYPE_CHECKING:
    from flask import Flask


QUEUE_NAME = 'results'


def listen_queue(app: "Flask"):
    """Listen for a new message in MQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', port=5672))

    try:
        channel = connection.channel()

        # Check if the queue has a message
        method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
        if method_frame:
            # If there is a message in the queue, consume it
            received_data = body.decode()
            app.logger.info(f"=== Received {received_data}")
            app.config['MESSAGE'] = received_data
        else:
            app.logger.info("No message in the queue. Stopping consumption.")
    finally:
        connection.close()
