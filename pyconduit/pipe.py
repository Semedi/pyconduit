from pyconduit.meta import builder
from pyconduit.pikaclient import PikaClient

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

    
    def send(self):
        self.client.send("test")

    def close(self):
        self.client.close()
