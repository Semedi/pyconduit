# pyconduit

pyconduit is a Python3 library to communicate processes efficiently regardless of the underlying technology.

Within the scope of the project, any type of tool that can be used to communicate data between two points can be included.

Some example may be:

* AMPQ protcocol using a rabbitmq broker
* Redis
* Kafka 
* AWS SQS or other cloud providers
* Python3 queues using multiprocessing

# Examples

### Emitter
```
import pyconduit

p = pyconduit.Pipe(
    pyconduit.EMITTER, 
    'ampq', 
    {
        'exchange': "test", 
        'topics': "topic01"
    }
)


p.send({"example": "data"})
```

### Receiver
```
import pyconduit

p = pyconduit.Pipe(
    pyconduit.RECEIVER, 
    'ampq', 
    {
        'exchange': "test", 
        'topics': "topic01"
    }
)

@p.get()
def receive(data):
    print("received:")
    print(data)



# Blocking call
p.consume()
```

# Contributing

To contribute pyconduit simpy upload your new pyconduit.meta.Client class with the proper interface already covered.

Any contribution is welcome.




