import pika

from pyconduit.meta import Client
import inspect
import hashlib


def _name_gen():
    seed = ''
    for p in inspect.stack():
        seed += p[1]

    name = hashlib.sha256(seed.encode('utf-8')).hexdigest()[0:10]

    return "queue.{}".format(name)

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
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host)
        )
        self.channel      = self.connection.channel()
        self.channel.exchange_declare(
            exchange      = config['exchange'],
            exchange_type = 'topic'
        )

    def send(self, message):

        topic = self.config['topics'][0]
        self.channel.basic_publish(
            exchange=self.config['exchange'],
            routing_key=topic,
            body=message
        )

    def receive(self):
        print("hola Mundo")

    def close(self):
        self.connection.close()
