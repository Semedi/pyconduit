from abc import ABCMeta, abstractmethod

class MetaClient(ABCMeta):
    _required_attrs = []

    def __call__(self, *args, **kwargs):
        obj = super(MetaClient, self).__call__(*args, **kwargs)
        for attr in obj._required_attrs:
            if not getattr(obj, attr):
                raise ValueError('required attribute (%s) not set' % attr_name)

        return obj


class BaseClient(object, metaclass=MetaClient):
    _required_attrs = ['mode']

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
    def __init__(self, mode):
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
