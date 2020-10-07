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
