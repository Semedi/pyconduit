import pika

from pyconduit.meta import Client

_opts = ['exchange', 'topic']
class PikaClient(Client):
    def __init__(self, mode, config):
        self.mode   = mode

        for k in _opts:
            if k not in config:
                raise AttributeError("attribute %s is mandatory inside config" % k)

        self.config = config

        if 'host' in config:
            host =  config['host']
        else:
            host = 'localhost'

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel    = self.connection.channel()
        self.channel.exchange_declare(
            exchange      = config['exchange'],
            exchange_type = 'topic'
        )

    def send(self, message):
        self.channel.basic_publish(
            exchange=self.config['exchange'],
            routing_key=self.config['topic'],
            body=message
        )

    def receive(self):
        print("hola Mundo")

    def close(self):
        self.connection.close()
