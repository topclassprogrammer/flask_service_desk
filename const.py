import os
from enum import Enum, auto

from dotenv import load_dotenv

load_dotenv()
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
TICKETS_EXCHANGE = "tickets_exchange"
TICKETS_QUEUE = "tickets_queue"
TICKETS_ROUTING_KEY = "ticket.created"


class StatusChoices(Enum):
    new = auto()
    in_progress = auto()
    done = auto()

