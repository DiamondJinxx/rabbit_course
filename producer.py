import pika 
import logging

from config import (
    rmq_config,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
    QUEUE_NAME
)

logger = logging.getLogger(__name__)

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
logger.info("[+] Connection over chanel established")

channel.exchange_declare(EXCHANGE_NAME, EXCHANGE_TYPE)
channel.queue_declare(QUEUE_NAME)
channel.queue_bind(
    queue=QUEUE_NAME, 
    exchange=EXCHANGE_NAME,
    routing_key="email.notifications"
)

def send_to_queue(
    channel, # pike doesn't export BlockingChannel type, so no type hint here
    exchange: str,
    routing_key: str,
    email: str,
    name: str,
    body: str
) -> None:
    msg = f"{email}\n{name}\n{body}"
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=msg
    )
    logger.info(f"[+] Message sent to queue {msg}")


send_to_queue(
    channel=channel,
    exchange=EXCHANGE_NAME,
    routing_key="email.notifications",
    email="abrakadabra_fn@yandex.ru",
    name="Joe Jones",
    body="LA Baby"
)

send_to_queue(
    channel=channel,
    exchange=EXCHANGE_NAME,
    routing_key="email.notifications",
    email="derty_ramires@email.ru",
    name="RAM",
    body="New albom presentation"
)

send_to_queue(
    channel=channel,
    exchange=EXCHANGE_NAME,
    routing_key="email.notifications",
    email="robot_battle@google.com",
    name="New battle",
    body="Battle publication"
)

try:
    channel.close()
    logger.info("[+] Connection closed")
except Exception as exc:
    logger.error(f"[-] Error during channel close {exc}")

