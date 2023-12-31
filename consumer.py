import sys, os
import pika 

from config import (
    rmq_config,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
    QUEUE_NAME
)


params = pika.ConnectionParameters(
    host=rmq_config.HOST,
    port=rmq_config.PORT,
    credentials=pika.PlainCredentials(
        username=rmq_config.USER,
        password=rmq_config.PASS
    )
)

print("start connection")
connection = pika.BlockingConnection(params)
channel = connection.channel()
print("[+] Connection over chanel established")

# check queue exists
channel.queue_declare(QUEUE_NAME)

def on_message(
    channel,
    method,
    properties,
    msg
) -> None:
    print(f"[+] Message recieved: {msg}")
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=on_message,
)

try:
    channel.start_consuming()
except Exception as exc:
    logger.error(f"Error diring consume queue {QUEUE_NAME}: #{exc}")
    try:
        sys.exit(1)
    except SystemExit:
        os._exit(1)
