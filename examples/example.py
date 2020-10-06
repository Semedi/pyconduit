import pyconduit

p = pyconduit.Pipe(
    pyconduit.EMITTER, 
    'ampq', 
    {
        'exchange': "a", 
        'topics': "test.topic"
    }
)
