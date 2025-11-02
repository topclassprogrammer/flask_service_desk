from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials
from pika.exchange_type import ExchangeType

from const import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_DEFAULT_VHOST, TICKETS_EXCHANGE, TICKETS_QUEUE, \
    TICKETS_ROUTING_KEY


def main():
    connection = BlockingConnection(ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host=RABBITMQ_DEFAULT_VHOST,
        credentials=PlainCredentials(username=RABBITMQ_DEFAULT_USER, password=RABBITMQ_DEFAULT_PASS)))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=10)

    channel.exchange_declare(TICKETS_EXCHANGE, ExchangeType.direct)
    channel.queue_declare(TICKETS_QUEUE)
    channel.queue_bind(exchange=TICKETS_EXCHANGE, queue=TICKETS_QUEUE, routing_key=TICKETS_ROUTING_KEY)

    def handle(channel, method, properties, body: bytes):
        print(f"Получено сообщение: {body.decode('utf-8')}")

    channel.basic_consume(queue=TICKETS_QUEUE, on_message_callback=handle, auto_ack=True)
    channel.start_consuming()


main()
