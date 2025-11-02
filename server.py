import json
import os

import flask
import pika
from flask import Flask, jsonify, request
from flask.cli import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask.views import MethodView
from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from const import StatusChoices, RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_VHOST, TICKETS_EXCHANGE, \
    TICKETS_ROUTING_KEY, RABBITMQ_PORT, RABBITMQ_HOST
from models import Session, User, Ticket
from schema import CreateTicket, CreateUser, UpdateUser

app = Flask(__name__)
jwt = JWTManager(app)
load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_VERIFY_SUB"] = False
bcrypt = Bcrypt(app)

@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: flask.Response):
    request.session.close()
    return http_response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError) -> flask.Response:
    http_response = jsonify({"status": "error", "message": error.message})
    http_response.status = error.status_code
    return http_response

def hash_password(password: str):
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    password = password.decode()
    return password


class UserView(MethodView):
    def get(self, user_id):
        user = get_user(user_id)
        return jsonify(user.json)

    def post(self):
        user_json = validate_user_json(request.json, CreateUser)
        user_json['password'] = hash_password(user_json['password'])
        user = User(**user_json)
        user_id = add_user(user)
        token = create_user_token(user_id)
        user.token = token
        request.session.commit()
        return jsonify({"status": f"User with id {user_id} created"}), 201

    @jwt_required()
    def patch(self, user_id):
        check_user_owner(user_id)
        user_json = validate_user_json(request.json, UpdateUser)
        if user_json.get('password'):
            user_json['password'] = hash_password(user_json['password'])
        user = get_user(user_id)
        for key, value in user_json.items():
            if value:
                setattr(user, key, value)
        request.session.commit()
        return jsonify({"status": f"User with id {user_id} updated"}), 200

    @jwt_required()
    def delete(self, user_id):
        check_user_owner(user_id)
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": f"User with id {user_id} deleted"}), 204

def get_user(user_id):
    user = request.session.get(User, user_id)
    if not user:
        raise HttpError(404, "User not found")
    return user

def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
        return user.id
    except IntegrityError:
        raise HttpError(409, "Username already exists")

def create_user_token(user_id: int):
    token = create_access_token(identity=user_id, expires_delta=False)
    return token

def check_user_owner(user_id: int):
    token_user_id = get_jwt_identity()
    if get_user(user_id) and token_user_id != user_id:
        raise HttpError(403, "You cannot modify this account as it does not belong to you")

def validate_user_json(json_data, schema_cls):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)


class TicketView(MethodView):
    @jwt_required()
    def post(self):
        json_data = validate_ticket_json(request.json, CreateTicket)
        ticket = Ticket(**json_data)
        add_ticket(ticket)
        connection = BlockingConnection(ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host=RABBITMQ_DEFAULT_VHOST,
            credentials=PlainCredentials(username=RABBITMQ_DEFAULT_USER, password=RABBITMQ_DEFAULT_PASS)))
        channel = connection.channel()
        channel.basic_publish(exchange=TICKETS_EXCHANGE, routing_key=TICKETS_ROUTING_KEY,
                              body=json.dumps(json_data), properties=pika.BasicProperties(delivery_mode=2))
        print(f"Отправлено сообщение: {json_data}")
        connection.close()
        return jsonify({"status": "created"}), 201

def add_ticket(ticket: Ticket):
    request.session.add(ticket)
    request.session.commit()
    return ticket.id

def validate_ticket_json(json_data, schema_cls):
    if not json_data.get('user') or not get_user(json_data['user']):
        raise HttpError(403, "Invalid user id")
    if not json_data.get('status') in StatusChoices._member_names_:
        raise HttpError(400, f"Invalid status. It must be one of the following values: {', '.join(StatusChoices._member_names_)}")
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)


ticket_view = TicketView.as_view("ticket_view")
user_view = UserView.as_view("user_view")
app.add_url_rule(rule='/user/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule(rule="/user", view_func=user_view, methods=['POST'])

app.add_url_rule(rule='/ticket/<int:ticket_id>', view_func=ticket_view, methods=['GET'])
app.add_url_rule(rule='/ticket', view_func=ticket_view, methods=['POST'])
