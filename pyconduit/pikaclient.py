import pika

from .base import BaseClient

_opts = ['mode']
class PikaClient(BaseClient):
    def __init__(self, mode):
        self.mode = mode
        print("hola Mundo")

    def send(self):
        print("hola Mundo")

    def receive(self):
        print("hola Mundo")

    def close(self):
        print("hola Mundo")
