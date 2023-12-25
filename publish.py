import argparse
import pika
import sys
from config import rmq_config

parser = argparse.ArgumentParser(description="Arguments for publishing to queue")
parser.add_argument(
    '-e', "--exchange",
    type=str,
    help="exchange for publication messages"
)
parser.add_argument(
    '-r', "--routing_key",
    type=str,
    help="routing key"
)
parser.add_argument(
    '-b', "--body",
    type=str,
    help="message body"
)
parser.add_argument(
    '-c', "--connection",
    type=str,
    help="connection to rabbitmq server, format 'host:port'"
)

arguments = parser.parse_args()
if arguments.connection is None:
    print('argument -c is require')
    sys.exit(2)
rmq_host, rmq_port = arguments.connection.split(":")


params = pika.ConnectionParameters(
    host=rmq_host,
    port=rmq_port,
    credentials=pika.PlainCredentials(
        username=rmq_config.USER,
        password=rmq_config.PASS
    )
)
connection = pika.BlockingConnection(params)
channel = connection.channel()
print("[+] Connection over chanel established")


def send_to_queue(
    channel, # pike doesn't export BlockingChannel type, so no type hint here
    exchange: str,
    routing_key: str,
    body: str
) -> None:
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=body
    )
    print(f"[+] Message sent to queue {body}")

send_to_queue(
    channel=channel,
    exchange=arguments.exchange,
    routing_key=arguments.routing_key,
    body=arguments.body
)

