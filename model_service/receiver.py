import time
from random import randint
from typing import TYPE_CHECKING

import pika

if TYPE_CHECKING:
    from logging import Logger


QUEUE_NAME = 'command'
QUEUE2_NAME = 'results'


def listen_queue(logger: "Logger"):
    """Listen for a new message in MQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', port=5672))

    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        def callback(ch, method, properties, body):
            received_data = body.decode()
            logger.info(f"=== Received {received_data}")

            start_model = 'start_model'
            if received_data == start_model:
                # sleep from 3 to 5 minutes and send 'done' message
                timeout = randint(3, 5) 
                start_time = time.time()

                # FIXME: should it be run in the separate thread to not block the consuming function?
                while True:
                    time.sleep(0.5)
                    logger.info('Model is working')
                    if time.time() - start_time > timeout:
                        break

                ch.basic_publish(
                    exchange='',
                    routing_key=QUEUE2_NAME,
                    body='model_finished'
                )
            logger.info("Model has finished the work")

        channel.basic_consume(queue=QUEUE_NAME,
                              auto_ack=True,
                              on_message_callback=callback)
        channel.start_consuming()
    finally:
        connection.close()
