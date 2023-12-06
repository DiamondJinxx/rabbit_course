import pika
import socket

from config import rmq_config


params = pika.ConnectionParameters(
    host=rmq_config.HOST,
    port=rmq_config.PORT,
    credentials=pika.PlainCredentials(
        username=rmq_config.USER,
        password=rmq_config.PASS
    )
)

connection = pika.BlockingConnection(params)
channel = connection.channel()


def on_message(
    ch,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body
) -> None:
    """ custom message handler """
    if method.redilivered:
        print(f"{method.delivery_tag} {body.decode('utf-8')}, Redilivered")
    else:
        channel.basic_nack(method.delivery_tag, requeue=True)


channel.basic_qos(prefetch_count=3)
consume_tag = channel.basic_consume(
    queue=rmq_config.DEFAULT_QUEUE,
    on_message_callback=on_message
)
print(consume_tag)

while True:
    connection.process_data_events()
