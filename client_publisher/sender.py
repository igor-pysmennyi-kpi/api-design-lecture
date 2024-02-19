import pika


QUEUE_NAME = 'command'


def send_msg(data, logger):
    """Send message to Broker."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', port=5672))
    logger.info('Connection established')

    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME,
                              body=bytes(data.encode()))
        logger.info(f'Sent {data}')

    finally:
        connection.close()
