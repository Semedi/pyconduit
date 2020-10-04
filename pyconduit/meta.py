from abc import ABCMeta, abstractmethod
from pyconduit.const import EMITTER, RECEIVER

_TYPE   = 'type'
_VALUES = 'values' 

class MetaClient(ABCMeta):
    _required_attrs = {}

    def __call__(self, *args, **kwargs):
        obj = super(MetaClient, self).__call__(*args, **kwargs)
        for attr in obj._required_attrs.keys():
            compile_op = obj._required_attrs[attr]
            if not getattr(obj, attr):
                raise ValueError("required attribute (%s) not set" % attr)

            t = compile_op[_TYPE]
            if type(getattr(obj, attr)) != t:
                raise TypeError("attribute (%s) should be (%s)" % (attr, str(t)))

            if _VALUES not in compile_op:
                continue

            v = compile_op[_VALUES]
            if getattr(obj, attr) not in v:
                raise AttributeError("attribute (%s) must include one of the following: %s" % (attr, str(v)))

        return obj

class Client(object, metaclass=MetaClient):
    _required_attrs = {
        'mode':   {
            _TYPE: str,
            _VALUES: [EMITTER, RECEIVER]
        },
        'config': {
            _TYPE: dict
        }
    }

    @classmethod
    def __subclass_hook__(cls, subclass):
        return (hasattr(subclass, 'send') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'receive') and 
                callable(subclass.extract_text) and 
                hasattr(subclass, 'close') and
                callable(subclass.close) or
                NotImplemented)

    @abstractmethod
    def __init__(self, mode, config):
        raise NotImplementedError

    @abstractmethod
    def send(self):
        raise NotImplementedError

    @abstractmethod
    def receive(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


def builder(f):
    def wrapper(*args, **kwargs):
        if args[0] not in [EMITTER, RECEIVER]:
            raise ValueError("mode should be emitter or receiver")

        i = f(*args, **kwargs)

        if not isinstance(i, Client):
            raise TypeError("instance (%i) not type Client" % str(i))

        return i
    return wrapper

