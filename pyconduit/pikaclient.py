import pika

from .meta import Client

_opts = ['mode']
class PikaClient(Client):
    def __init__(self, mode, config):
        self.mode   = mode
        self.config = config

        if 'host' in config:
            host =  config['host']
        else:
            host = 'localhost'

        connection = pika.BlockingConnection(pika.ConnectionParameters(host))

    def send(self):
        print("hola Mundo")

    def receive(self):
        print("hola Mundo")

    def close(self):
        print("hola Mundo")
