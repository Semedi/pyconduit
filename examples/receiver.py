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



p.consume()
