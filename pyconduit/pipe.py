from pyconduit.meta import builder
from pyconduit.pikaclient import PikaClient

import json

# Client Factory:
@builder
def _ampq(mode, config):
    return PikaClient(mode, config)

_factory = {
    'ampq': _ampq
}

class Pipe:
    def __init__(self, mode, client, config):
        if client not in _factory.keys():
            raise ValueError("client (%s) does not exist" % client)
            
        self.client = _factory[client](mode, config)

    
    def send(self, data):
        if type(data) != dict:
            raise RuntimeError("please pack your message into a dict object")

        message = json.dumps(data)

        self.client.send(message)


    def get(self):
        def decorator(f):
            self.client.set_manager(f)

            return f
        return decorator

    def consume(self):
        self.client.receive()

    def close(self):
        self.client.close()
