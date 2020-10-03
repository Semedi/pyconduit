import pika

from .meta import Client

_opts = ['mode']
class PikaClient(Client):
    def __init__(self, mode, config):
        self.mode   = mode
        self.config = config
        print("hola Mundo")

    def send(self):
        print("hola Mundo")

    def receive(self):
        print("hola Mundo")

    def close(self):
        print("hola Mundo")
