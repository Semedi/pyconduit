import pika


from pyconduit.meta import Client
from pyconduit.const import EMITTER, RECEIVER

import inspect
import hashlib

import time

# Private namespace
def _name_gen():
    seed = ''
    for p in inspect.stack():
        seed += p[1]

    name = hashlib.sha256(seed.encode('utf-8')).hexdigest()[0:10]

    return "queue.{}".format(name)

def _connect(host='localhost'):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host)
        )
    except pika.exceptions.AMQPConnectionError as e:
        print("couldn't connect to {}".format(host))
        exit(1)

    return connection

def _exchange_check(ch, exchange):
    ch.exchange_declare(
        exchange      = exchange,
        exchange_type = 'topic'
    )


class Manager():
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, ch, method, properties, body):
        print(" [x] Received {}:{} - {}".format(method.routing_key, body.decode(), time.time()))

        self.callback("test")

        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

_opts = ['exchange', 'topics']
class PikaClient(Client):
    def __init__(self, mode, config):

        for k in _opts:
            if k not in config:
                raise AttributeError("attribute %s is mandatory inside config" % k)

        self.mode   = mode
        self.config = config

        if type(config['topics']) != list:
            self.config['topics'] = [self.config['topics']]

        host = config.get('host', 'localhost')

        self.connection = _connect(host)
        self.channel    = self.connection.channel()

        _exchange_check(self.channel, config.get('exchange'))

        if mode == EMITTER:
            print("hola")

    def send(self, message):

        topic = self.config['topics'][0]
        self.channel.basic_publish(
            exchange=self.config['exchange'],
            routing_key=topic,
            body=message
        )

    def receive(self):

        def decorator(f):
            self.manager = Manager(f)

            return f
        return decorator
    
    def run():
        print("Hola Mundo")

    def close(self):
        self.connection.close()
